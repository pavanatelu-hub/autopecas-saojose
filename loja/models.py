
from django.db import models

# Create your models here.
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='produtos/%Y/%m/%d', blank=True)
    disponivel = models.BooleanField(default=True)
    
    # Detalhes essenciais para autopeças
    codigo_original = models.CharField(max_length=50, blank=True) # Ex: Part Number
    compatibilidade = models.TextField(help_text="Ex: Gol G5, Fox 2012...")

    def __str__(self):
        return self.nome
    
    # Peso em kg, dimensões em cm
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=0.5)
    comprimento = models.DecimalField(max_digits=5, decimal_places=2, default=16.0)
    largura = models.DecimalField(max_digits=5, decimal_places=2, default=11.0)
    altura = models.DecimalField(max_digits=5, decimal_places=2, default=2.0)