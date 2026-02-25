from django.contrib import admin
from .models import Categoria, Produto

# Aqui NÃO pode ter parênteses no final de Categoria e Produto
admin.site.register(Categoria)
admin.site.register(Produto)