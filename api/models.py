from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

class Curso(models.Model):
    NIVEL_CHOICES = (
        ('B', 'Básico'),
        ('I', 'Intermediário'),
        ('A', 'Avançado'),
    )
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='cursos')
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, default='B')
    carga_horaria = models.PositiveIntegerField()
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-data_publicacao']

class ConfiguracaoIA(models.Model):
    MODELO_CHOICES = (
        # Modelos DeepSeek
        ('deepseek-chat', 'DeepSeek Chat'),
        ('deepseek-lite', 'DeepSeek Lite'),
        ('deepseek-v2', 'DeepSeek V2'),
        
        # Modelos OpenAI (mantidos para compatibilidade)
        ('gpt-3.5-turbo', 'GPT-3.5 Turbo'),
        ('gpt-4', 'GPT-4'),
        ('gpt-4-turbo', 'GPT-4 Turbo'),
    )
    
    PROVEDOR_CHOICES = (
        ('deepseek', 'DeepSeek'),
        ('openai', 'OpenAI'),
    )
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    provedor = models.CharField(max_length=20, choices=PROVEDOR_CHOICES, default='deepseek')
    modelo = models.CharField(max_length=50, choices=MODELO_CHOICES, default='deepseek-chat')
    temperatura = models.FloatField(default=0.7)
    max_tokens = models.PositiveIntegerField(default=1000)
    chave_api = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Configuração de IA'
        verbose_name_plural = 'Configurações de IA'
        ordering = ['nome']

class Interacao(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='interacoes')
    configuracao_ia = models.ForeignKey(ConfiguracaoIA, on_delete=models.SET_NULL, null=True, related_name='interacoes')
    pergunta = models.TextField()
    resposta = models.TextField()
    tokens_utilizados = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Interação {self.id} - {self.curso.titulo}"
    
    class Meta:
        verbose_name = 'Interação'
        verbose_name_plural = 'Interações'
        ordering = ['-data_criacao']
