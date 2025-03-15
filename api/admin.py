from django.contrib import admin
from .models import Categoria, Curso, ConfiguracaoIA, Interacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_criacao')
    search_fields = ('nome', 'descricao')
    list_filter = ('data_criacao',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'nivel', 'carga_horaria', 'ativo', 'data_publicacao')
    search_fields = ('titulo', 'descricao', 'categoria__nome')
    list_filter = ('nivel', 'ativo', 'categoria', 'data_publicacao')
    date_hierarchy = 'data_publicacao'

@admin.register(ConfiguracaoIA)
class ConfiguracaoIAAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modelo', 'temperatura', 'max_tokens', 'ativo', 'data_criacao')
    search_fields = ('nome', 'descricao', 'modelo')
    list_filter = ('modelo', 'ativo', 'data_criacao')
    date_hierarchy = 'data_criacao'

@admin.register(Interacao)
class InteracaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'configuracao_ia', 'tokens_utilizados', 'data_criacao')
    search_fields = ('pergunta', 'resposta', 'curso__titulo')
    list_filter = ('curso', 'configuracao_ia', 'data_criacao')
    date_hierarchy = 'data_criacao'
    readonly_fields = ('pergunta', 'resposta', 'tokens_utilizados', 'data_criacao')
