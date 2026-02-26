from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Importamos todas as funções que criamos na views da loja
from loja.views import vitrine, detalhe_produto, calcular_frete, checkout, finalizar_pedido, criar_adm_provisorio

urlpatterns = [
    # Painel do Administrador
    path('admin/', admin.site.urls),
    
    # Página inicial (Vitrine)
    path('', vitrine, name='vitrine'),
    
    # Página de detalhes de cada peça
    path('produto/<int:id>/', detalhe_produto, name='detalhe_produto'),
    
    # Rota invisível que faz o cálculo do frete
    path('calcular-frete/', calcular_frete, name='calcular_frete'),
    path('checkout/<int:id>/', checkout, name='checkout'),
    path('finalizar_pedido/<int:id>/', finalizar_pedido, name='finalizar_pedido'),
  path('setup-adm/', view=criar_adm_provisorio),
]

# Configuração para as imagens das peças aparecerem
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)