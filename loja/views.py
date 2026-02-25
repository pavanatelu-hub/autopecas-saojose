import requests
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from .models import Produto, Categoria
from django.db.models import Q

# --- VITRINE ---
def vitrine(request):
    categorias = Categoria.objects.all()
    nome_produto = request.GET.get('busca')
    categoria_id = request.GET.get('categoria')
    produtos = Produto.objects.all()

    if nome_produto:
        produtos = produtos.filter(Q(nome__icontains=nome_produto) | Q(compatibilidade__icontains=nome_produto))
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    return render(request, 'loja/vitrine.html', {'produtos': produtos, 'categorias': categorias})

# --- DETALHE DO PRODUTO ---
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'loja/detalhe.html', {'produto': produto})

# --- MOTOR DE FRETE (MELHOR ENVIO) ---
def calcular_frete(request):
    cep_destino = request.GET.get('cep')
    produto_id = request.GET.get('produto_id')
    
    if not cep_destino:
        return JsonResponse({'opcoes': []})

    # Limpa o CEP
    cep_destino = ''.join(filter(str.isdigit, cep_destino))
    produto = get_object_or_404(Produto, id=produto_id)

    payload = {
        "from": {"postal_code": settings.CEP_ORIGEM},
        "to": {"postal_code": cep_destino},
        "products": [
            {
                "id": str(produto.id),
                "width": float(produto.largura),
                "height": float(produto.altura),
                "length": float(produto.comprimento),
                "weight": float(produto.peso),
                "insurance_value": float(produto.preco),
                "quantity": 1
            }
        ]
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.MELHOR_ENVIO_TOKEN}",
        "User-Agent": "Autopeças São José (contato@seusite.com)"
    }

    try:
        response = requests.post(settings.MELHOR_ENVIO_URL, json=payload, headers=headers)
        print(f"RESPOSTA DA API FRETE: {response.text}") # Ver no terminal
        data = response.json()
        opcoes = []
        for servico in data:
            if "error" not in servico and "price" in servico:
                opcoes.append({
                    'nome': servico['name'],
                    'valor': servico['price'],
                    'prazo': f"{servico['delivery_range']['min']} a {servico['delivery_range']['max']} dias"
                })
        return JsonResponse({'opcoes': opcoes})
    except Exception as e:
        print(f"Erro no frete: {e}")
        return JsonResponse({'opcoes': []})

# --- CHECKOUT E PAGAMENTO (ASAAS) ---
def checkout(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'loja/checkout.html', {'produto': produto})

def finalizar_pedido(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    if request.method == "POST":
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf').replace('.', '').replace('-', '')
        email = request.POST.get('email')

        headers = {"access_token": settings.ASAAS_API_KEY}
        
        # 1. Criar Cliente
        cliente_data = {"name": nome, "cpfCnpj": cpf, "email": email}
        c_res = requests.post(f"{settings.ASAAS_URL}/customers", json=cliente_data, headers=headers).json()
        cliente_id = c_res.get('id')

        # 2. Criar Cobrança Pix
        cobranca_data = {
            "customer": cliente_id,
            "billingType": "PIX",
            "value": float(produto.preco),
            "dueDate": "2026-12-31",
            "description": f"Compra: {produto.nome}"
        }
        cob_res = requests.post(f"{settings.ASAAS_URL}/payments", json=cobranca_data, headers=headers).json()
        cobranca_id = cob_res.get('id')

        # 3. Pegar QR Code
        pix_res = requests.get(f"{settings.ASAAS_URL}/payments/{cobranca_id}/pixQrCode", headers=headers).json()
        
        return render(request, 'loja/pagamento.html', {
            'pix_code': pix_res.get('payload'),
            'qrcode_base64': pix_res.get('encodedImage')
        })