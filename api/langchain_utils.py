import os
import time
import logging
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from .models import ConfiguracaoIA, Curso, Interacao

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

def get_llm_from_config(config):
    """
    Cria uma instância de LLM com base na configuração fornecida.
    """
    logger.debug(f"Inicializando LLM com provedor: {config.provedor}, modelo: {config.modelo}")
    
    if config.provedor == 'deepseek':
        # Usar a chave da configuração ou a chave do ambiente para DeepSeek
        api_key = config.chave_api or os.getenv("DEEPSEEK_API_KEY")
        logger.debug(f"Usando API key DeepSeek (primeiros 5 caracteres): {api_key[:5]}...")
        
        # Criar o modelo LLM DeepSeek
        try:
            logger.debug("Tentando inicializar ChatDeepSeek...")
            llm = ChatDeepSeek(
                model=config.modelo,
                temperature=config.temperatura,
                max_tokens=config.max_tokens,
                api_key=api_key,
                request_timeout=60,  # Aumentando o timeout para 60 segundos
            )
            logger.debug("ChatDeepSeek inicializado com sucesso")
            return llm
        except Exception as e:
            logger.error(f"Erro ao inicializar DeepSeek: {str(e)}")
            return None
    else:  # OpenAI como fallback
        # Usar a chave da configuração ou a chave do ambiente para OpenAI
        api_key = config.chave_api or os.getenv("OPENAI_API_KEY")
        logger.debug(f"Usando API key OpenAI (primeiros 5 caracteres): {api_key[:5] if api_key else 'Não definida'}...")
        
        # Criar o modelo LLM OpenAI
        try:
            logger.debug("Tentando inicializar ChatOpenAI...")
            llm = ChatOpenAI(
                model=config.modelo,
                temperature=config.temperatura,
                max_tokens=config.max_tokens,
                api_key=api_key,
                request_timeout=60,  # Aumentando o timeout para 60 segundos
            )
            logger.debug("ChatOpenAI inicializado com sucesso")
            return llm
        except Exception as e:
            logger.error(f"Erro ao inicializar OpenAI: {str(e)}")
            return None

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
    if llm is None:
        raise ValueError(f"Não foi possível inicializar o modelo de IA com o provedor {config.provedor}.")
    
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
    start_time = time.time()
    logger.debug(f"Iniciando process_question para curso_id: {curso_id}, pergunta: {pergunta[:50]}...")
    
    def get_resposta_simulada(curso, pergunta):
        """Função auxiliar para gerar resposta simulada mais elaborada"""
        logger.debug("Gerando resposta simulada...")
        pergunta_lower = pergunta.lower()
        
        # Respostas simuladas baseadas em palavras-chave na pergunta
        if "python" in pergunta_lower and ("conceitos" in pergunta_lower or "básicos" in pergunta_lower or "aprender" in pergunta_lower):
            return """
            Para começar a aprender Python, você deve focar nos seguintes conceitos básicos:

            1. **Sintaxe básica**: Como escrever comandos Python corretamente
            2. **Variáveis e tipos de dados**: Inteiros, floats, strings, booleanos, listas, tuplas, dicionários
            3. **Operadores**: Aritméticos, de comparação, lógicos
            4. **Estruturas de controle**: if/else, loops (for, while)
            5. **Funções**: Como definir e chamar funções, argumentos, retorno
            6. **Manipulação de strings**: Métodos de string, formatação
            7. **Trabalhando com listas e dicionários**: Métodos e operações comuns
            8. **Manipulação de arquivos**: Leitura e escrita em arquivos
            9. **Tratamento de exceções**: try/except
            10. **Módulos e pacotes**: Como importar e usar bibliotecas

            No curso '{}', você aprenderá esses conceitos fundamentais através de explicações claras e exercícios práticos. É recomendado praticar código todos os dias e trabalhar em pequenos projetos para fixar o conhecimento.
            """.format(curso.titulo)
        
        elif "função" in pergunta_lower or "funções" in pergunta_lower:
            return """
            Funções em Python são blocos de código reutilizáveis que realizam tarefas específicas. Elas ajudam a organizar seu código e evitar repetição.

            Para definir uma função em Python:

            ```python
            def nome_da_funcao(parametro1, parametro2):
                # Corpo da função
                resultado = parametro1 + parametro2
                return resultado
            ```

            Características importantes das funções em Python:
            - Usamos a palavra-chave `def` para defini-las
            - Podem receber parâmetros (dados de entrada)
            - Podem retornar valores com a palavra-chave `return`
            - Podem ter parâmetros opcionais com valores padrão
            - Podem ser documentadas com docstrings

            No curso '{}', você aprenderá como escrever funções eficientes e quando usá-las apropriadamente.
            """.format(curso.titulo)
        
        elif "loop" in pergunta_lower or "for" in pergunta_lower or "while" in pergunta_lower:
            return """
            Loops em Python permitem executar um bloco de código várias vezes. Os dois tipos principais são:

            **Loop for**: Usado para iterar sobre uma sequência (lista, tupla, string, etc.)
            ```python
            for item in lista:
                print(item)
            ```

            **Loop while**: Executa enquanto uma condição for verdadeira
            ```python
            contador = 0
            while contador < 5:
                print(contador)
                contador += 1
            ```

            Recursos adicionais:
            - `range()`: Gera sequências numéricas para loops
            - `break`: Sai imediatamente do loop
            - `continue`: Pula para a próxima iteração
            - Compreensão de lista: `[x*2 for x in lista]`

            No curso '{}', exploramos estes conceitos com exercícios práticos para fixação.
            """.format(curso.titulo)
        
        elif "lista" in pergunta_lower or "dicionário" in pergunta_lower or "estrutura" in pergunta_lower:
            return """
            Python tem várias estruturas de dados importantes:

            **Listas**: Coleções ordenadas e mutáveis
            ```python
            frutas = ['maçã', 'banana', 'laranja']
            frutas.append('uva')  # Adiciona item
            ```

            **Tuplas**: Coleções ordenadas e imutáveis
            ```python
            coordenadas = (10, 20)
            ```

            **Dicionários**: Pares de chave-valor
            ```python
            pessoa = {
                'nome': 'João',
                'idade': 30,
                'profissão': 'desenvolvedor'
            }
            ```

            **Conjuntos (Sets)**: Coleções não ordenadas de itens únicos
            ```python
            cores = {'vermelho', 'verde', 'azul'}
            ```

            Cada estrutura tem seu próprio conjunto de métodos e casos de uso ideais, que são detalhados no curso '{}'.
            """.format(curso.titulo)
        
        else:
            # Resposta genérica para outras perguntas
            return f"""
            Esta é uma resposta simulada para sua pergunta sobre '{pergunta}'.
            
            No curso '{curso.titulo}', abordamos esse e outros tópicos relacionados. 
            A descrição do curso menciona:
            
            "{curso.descricao[:300]}..."
            
            Para obter respostas mais precisas e detalhadas, seria necessário configurar uma integração com um modelo de IA como o DeepSeek ou OpenAI através do painel administrativo.
            """
    
    try:
        # Obter o curso
        logger.debug(f"Tentando obter curso com ID {curso_id}...")
        curso = Curso.objects.get(id=curso_id)
        logger.debug(f"Curso encontrado: {curso.titulo}")
        
        # Obter a configuração
        config = None
        if configuracao_id:
            try:
                logger.debug(f"Tentando obter configuração com ID {configuracao_id}...")
                config = ConfiguracaoIA.objects.get(id=configuracao_id, ativo=True)
                logger.debug(f"Configuração encontrada: {config.nome}")
            except ConfiguracaoIA.DoesNotExist:
                logger.warning(f"Configuração ID {configuracao_id} não encontrada ou inativa.")
                pass
        
        if not config:
            logger.debug("Tentando obter primeira configuração ativa...")
            config = ConfiguracaoIA.objects.filter(ativo=True).first()
            if config:
                logger.debug(f"Configuração ativa encontrada: {config.nome}")
            else:
                logger.warning("Nenhuma configuração ativa encontrada.")
        
        # Se não houver configuração ou se a configuração for inválida, usar resposta simulada
        if not config:
            logger.info("Usando modo de resposta simulada devido à falta de configuração.")
            resposta = get_resposta_simulada(curso, pergunta)
            
            # Estimar tokens (simplificado)
            tokens_utilizados = len(pergunta.split()) + len(resposta.split())
            
            # Salvar a interação com configuração nula
            interacao = Interacao.objects.create(
                curso=curso,
                configuracao_ia=None,
                pergunta=pergunta,
                resposta=resposta,
                tokens_utilizados=tokens_utilizados
            )
            
            elapsed_time = time.time() - start_time
            logger.debug(f"Resposta simulada gerada em {elapsed_time:.2f} segundos")
            
            return {
                "resposta": resposta,
                "interacao_id": interacao.id,
                "tokens_utilizados": tokens_utilizados,
                "modo": "simulado"
            }
        
        try:
            # Tentar criar e executar a cadeia
            logger.debug("Criando cadeia para o curso...")
            chain_start_time = time.time()
            chain = create_chain_for_course(curso, config)
            logger.debug(f"Cadeia criada em {time.time() - chain_start_time:.2f} segundos")
            
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
            logger.debug("Executando a cadeia com a pergunta...")
            invoke_start_time = time.time()
            result = chain.invoke(inputs)
            invoke_time = time.time() - invoke_start_time
            logger.debug(f"Cadeia executada em {invoke_time:.2f} segundos")
            
            resposta = result.get("text", "")
            logger.debug(f"Resposta obtida com {len(resposta)} caracteres")
            
        except Exception as e:
            logger.error(f"Erro ao executar a cadeia: {str(e)}")
            resposta = get_resposta_simulada(curso, pergunta)
            logger.debug("Usando resposta simulada devido a erro na execução")
        
        # Estimar tokens (simplificado)
        tokens_utilizados = len(pergunta.split()) + len(resposta.split())
        
        # Salvar a interação
        logger.debug("Salvando interação no banco de dados...")
        interacao = Interacao.objects.create(
            curso=curso,
            configuracao_ia=config,
            pergunta=pergunta,
            resposta=resposta,
            tokens_utilizados=tokens_utilizados
        )
        
        elapsed_time = time.time() - start_time
        logger.debug(f"process_question concluído em {elapsed_time:.2f} segundos")
        
        return {
            "resposta": resposta,
            "interacao_id": interacao.id,
            "tokens_utilizados": tokens_utilizados
        }
        
    except Curso.DoesNotExist:
        logger.error(f"Curso ID {curso_id} não encontrado")
        return {"error": "Curso não encontrado."}
    except Exception as e:
        logger.error(f"Erro não tratado em process_question: {str(e)}")
        return {"error": str(e)} 