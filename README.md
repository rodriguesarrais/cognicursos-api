# CogniCursos API

API REST para gerenciamento de cursos e categorias, desenvolvida com Django Rest Framework. Inclui integração com modelos de IA via LangChain para responder perguntas sobre os cursos, utilizando DeepSeek como provedor principal.

## Tecnologias Utilizadas

- Python 3.x
- Django 5.x
- Django Rest Framework 3.x
- SQLite
- LangChain
- DeepSeek API
- OpenAI API (como alternativa)

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/cognicursos-api.git
cd cognicursos-api
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave de API do DeepSeek: `DEEPSEEK_API_KEY=sua_chave_aqui`
   - Opcionalmente, adicione sua chave de API da OpenAI: `OPENAI_API_KEY=sua_chave_aqui`

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## Endpoints da API

### Categorias

- `GET /api/categorias/` - Listar todas as categorias
- `POST /api/categorias/` - Criar uma nova categoria
- `GET /api/categorias/{id}/` - Obter detalhes de uma categoria
- `PUT /api/categorias/{id}/` - Atualizar uma categoria
- `DELETE /api/categorias/{id}/` - Excluir uma categoria

### Cursos

- `GET /api/cursos/` - Listar todos os cursos
- `POST /api/cursos/` - Criar um novo curso
- `GET /api/cursos/{id}/` - Obter detalhes de um curso
- `PUT /api/cursos/{id}/` - Atualizar um curso
- `DELETE /api/cursos/{id}/` - Excluir um curso
- `POST /api/cursos/{id}/perguntar/` - Fazer uma pergunta sobre o curso usando IA

### Configurações de IA

- `GET /api/configuracoes-ia/` - Listar todas as configurações de IA
- `POST /api/configuracoes-ia/` - Criar uma nova configuração de IA
- `GET /api/configuracoes-ia/{id}/` - Obter detalhes de uma configuração
- `PUT /api/configuracoes-ia/{id}/` - Atualizar uma configuração
- `DELETE /api/configuracoes-ia/{id}/` - Excluir uma configuração

### Interações

- `GET /api/interacoes/` - Listar todas as interações com IA
- `GET /api/interacoes/{id}/` - Obter detalhes de uma interação

### Filtros Disponíveis

- Cursos por categoria: `GET /api/cursos/?categoria={id}`
- Cursos por nível: `GET /api/cursos/?nivel={B|I|A}`
- Cursos ativos/inativos: `GET /api/cursos/?ativo={true|false}`
- Busca por texto: `GET /api/cursos/?search={termo}`
- Interações por curso: `GET /api/interacoes/?curso={id}`

## Funcionalidade de IA com LangChain e DeepSeek

A API inclui integração com modelos de IA através do LangChain e DeepSeek para responder perguntas sobre os cursos. Para usar esta funcionalidade:

1. Crie uma configuração de IA no painel administrativo ou via API
   - Escolha o provedor (DeepSeek ou OpenAI)
   - Selecione o modelo desejado
   - Configure a temperatura e o número máximo de tokens
   - Adicione sua chave de API

2. Faça uma requisição POST para `/api/cursos/{id}/perguntar/` com o seguinte corpo:

```json
{
  "pergunta": "Qual é o conteúdo deste curso?",
  "configuracao_id": 1,  // Opcional, usa a primeira configuração ativa se não for fornecido
  "contexto": "Informações adicionais para contextualizar a pergunta"  // Opcional
}
```

A resposta incluirá:
- A resposta gerada pelo modelo de IA
- O ID da interação salva
- A quantidade estimada de tokens utilizados

## Modelos DeepSeek Disponíveis

- `deepseek-chat` - Modelo de chat padrão do DeepSeek
- `deepseek-lite` - Versão mais leve do modelo DeepSeek
- `deepseek-v2` - Versão 2 do modelo DeepSeek

Interface de administração: http://127.0.0.1:8003/admin/
API Root: http://127.0.0.1:8003/api/
Endpoints de categorias: http://127.0.0.1:8003/api/categorias/
Endpoints de cursos: http://127.0.0.1:8003/api/cursos/
Endpoints de configurações de IA: http://127.0.0.1:8003/api/configuracoes-ia/
Endpoints de interações: http://127.0.0.1:8003/api/interacoes/
Para usar a funcionalidade de IA com o DeepSeek, você precisará:
* Criar uma categoria e um curso
* Criar uma configuração de IA com sua chave do DeepSeek
* Fazer uma requisição POST para /api/cursos/{id}/perguntar/ com a pergunta