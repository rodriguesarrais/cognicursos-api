import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from .models import ConfiguracaoIA, Curso, Interacao

# Carregar variáveis de ambiente
load_dotenv()

def get_llm_from_config(config):
    """
    Cria uma instância de LLM com base na configuração fornecida.
    """
    if config.provedor == 'deepseek':
        # Usar a chave da configuração ou a chave do ambiente para DeepSeek
        api_key = config.chave_api or os.getenv("DEEPSEEK_API_KEY")
        
        # Criar o modelo LLM DeepSeek
        llm = ChatDeepSeek(
            model=config.modelo,
            temperature=config.temperatura,
            max_tokens=config.max_tokens,
            deepseek_api_key=api_key,
        )
    else:  # OpenAI como fallback
        # Usar a chave da configuração ou a chave do ambiente para OpenAI
        api_key = config.chave_api or os.getenv("OPENAI_API_KEY")
        
        # Criar o modelo LLM OpenAI
        llm = ChatOpenAI(
            model=config.modelo,
            temperature=config.temperatura,
            max_tokens=config.max_tokens,
            openai_api_key=api_key,
        )
    
    return llm

def create_chain_for_course(curso, config=None):
    """
    Cria uma cadeia LangChain para um curso específico.
    """
    # Se não for fornecida uma configuração, usar a primeira configuração ativa
    if not config:
        config = ConfiguracaoIA.objects.filter(ativo=True).first()
        if not config:
            raise ValueError("Nenhuma configuração de IA ativa encontrada.")
    
    # Obter o LLM
    llm = get_llm_from_config(config)
    
    # Criar um template de prompt para o curso
    template = """
    Você é um assistente de aprendizado para o curso: {curso_titulo}.
    
    Informações sobre o curso:
    - Título: {curso_titulo}
    - Descrição: {curso_descricao}
    - Nível: {curso_nivel}
    - Categoria: {curso_categoria}
    
    Contexto adicional: {contexto}
    
    Histórico da conversa:
    {chat_history}
    
    Pergunta do aluno: {pergunta}
    
    Sua resposta deve ser educativa, clara e útil. Forneça exemplos quando apropriado.
    Resposta:
    """
    
    # Criar o prompt
    prompt = PromptTemplate(
        input_variables=["curso_titulo", "curso_descricao", "curso_nivel", 
                         "curso_categoria", "contexto", "chat_history", "pergunta"],
        template=template
    )
    
    # Criar memória para manter o histórico da conversa
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="pergunta")
    
    # Criar a cadeia
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    return chain

def process_question(curso_id, pergunta, configuracao_id=None, contexto=""):
    """
    Processa uma pergunta usando LangChain e salva a interação.
    """
    try:
        # Obter o curso
        curso = Curso.objects.get(id=curso_id)
        
        # Obter a configuração
        if configuracao_id:
            config = ConfiguracaoIA.objects.get(id=configuracao_id, ativo=True)
        else:
            config = ConfiguracaoIA.objects.filter(ativo=True).first()
            if not config:
                return {"error": "Nenhuma configuração de IA ativa encontrada."}
        
        # Criar a cadeia
        chain = create_chain_for_course(curso, config)
        
        # Preparar os inputs
        nivel_texto = dict(Curso.NIVEL_CHOICES).get(curso.nivel, "")
        inputs = {
            "curso_titulo": curso.titulo,
            "curso_descricao": curso.descricao,
            "curso_nivel": nivel_texto,
            "curso_categoria": curso.categoria.nome,
            "contexto": contexto,
            "pergunta": pergunta
        }
        
        # Executar a cadeia
        result = chain.invoke(inputs)
        resposta = result.get("text", "")
        
        # Estimar tokens (simplificado)
        tokens_utilizados = len(pergunta.split()) + len(resposta.split())
        
        # Salvar a interação
        interacao = Interacao.objects.create(
            curso=curso,
            configuracao_ia=config,
            pergunta=pergunta,
            resposta=resposta,
            tokens_utilizados=tokens_utilizados
        )
        
        return {
            "resposta": resposta,
            "interacao_id": interacao.id,
            "tokens_utilizados": tokens_utilizados
        }
        
    except Curso.DoesNotExist:
        return {"error": "Curso não encontrado."}
    except ConfiguracaoIA.DoesNotExist:
        return {"error": "Configuração de IA não encontrada ou inativa."}
    except Exception as e:
        return {"error": str(e)} 