from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Categoria, Curso, ConfiguracaoIA, Interacao

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'data_criacao']

class CursoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.ReadOnlyField(source='categoria.nome')
    
    class Meta:
        model = Curso
        fields = [
            'id', 'titulo', 'descricao', 'data_publicacao', 
            'data_atualizacao', 'categoria', 'categoria_nome', 
            'nivel', 'carga_horaria', 'ativo'
        ]

class ConfiguracaoIASerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoIA
        fields = [
            'id', 'nome', 'descricao', 'provedor', 'modelo', 'temperatura', 
            'max_tokens', 'chave_api', 'ativo', 'data_criacao', 
            'data_atualizacao'
        ]
        extra_kwargs = {
            'chave_api': {'write_only': True}  # Não retorna a chave API nas respostas
        }

class InteracaoSerializer(serializers.ModelSerializer):
    curso_titulo = serializers.ReadOnlyField(source='curso.titulo')
    configuracao_nome = serializers.ReadOnlyField(source='configuracao_ia.nome')
    
    class Meta:
        model = Interacao
        fields = [
            'id', 'curso', 'curso_titulo', 'configuracao_ia', 
            'configuracao_nome', 'pergunta', 'resposta', 
            'tokens_utilizados', 'data_criacao'
        ]

class PerguntaSerializer(serializers.Serializer):
    curso_id = serializers.IntegerField(required=False)
    configuracao_id = serializers.IntegerField(required=False)
    pergunta = serializers.CharField(max_length=2000)
    contexto = serializers.CharField(max_length=5000, required=False) 