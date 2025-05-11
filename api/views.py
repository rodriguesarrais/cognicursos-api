from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Curso, ConfiguracaoIA, Interacao
from .serializers import (
    CategoriaSerializer, CursoSerializer, 
    ConfiguracaoIASerializer, InteracaoSerializer,
    PerguntaSerializer, UserSerializer
)
from .langchain_utils import process_question

# Create your views here.

# Listar e Criar Usuários
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Obter, Atualizar e Excluir Usuário
class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar categorias.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_criacao']

class CursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar cursos.
    """
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descricao', 'categoria__nome']
    ordering_fields = ['titulo', 'data_publicacao', 'carga_horaria', 'nivel']
    
    def get_queryset(self):
        """
        Permite filtrar cursos por categoria e nível.
        """
        queryset = Curso.objects.all()
        categoria_id = self.request.query_params.get('categoria', None)
        nivel = self.request.query_params.get('nivel', None)
        ativo = self.request.query_params.get('ativo', None)
        
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        if nivel:
            queryset = queryset.filter(nivel=nivel)
        if ativo is not None:
            ativo_bool = ativo.lower() == 'true'
            queryset = queryset.filter(ativo=ativo_bool)
            
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def perguntar(self, request, pk=None):
        """
        Endpoint para fazer perguntas sobre um curso específico.
        """
        curso = self.get_object()
        serializer = PerguntaSerializer(data=request.data)
        
        if serializer.is_valid():
            # Substituir o curso_id do serializer pelo ID do curso da URL
            curso_id = curso.id
            pergunta = serializer.validated_data['pergunta']
            configuracao_id = serializer.validated_data.get('configuracao_id')
            contexto = serializer.validated_data.get('contexto', '')
            
            # Processar a pergunta
            result = process_question(
                curso_id=curso_id,
                pergunta=pergunta,
                configuracao_id=configuracao_id,
                contexto=contexto
            )
            
            if 'error' in result:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(result)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfiguracaoIAViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar configurações de IA.
    """
    queryset = ConfiguracaoIA.objects.all()
    serializer_class = ConfiguracaoIASerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao', 'modelo']
    ordering_fields = ['nome', 'data_criacao']

class InteracaoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para visualizar interações com IA.
    """
    queryset = Interacao.objects.all()
    serializer_class = InteracaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pergunta', 'resposta', 'curso__titulo']
    ordering_fields = ['data_criacao']
    
    def get_queryset(self):
        """
        Permite filtrar interações por curso.
        """
        queryset = Interacao.objects.all()
        curso_id = self.request.query_params.get('curso', None)
        
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
            
        return queryset
