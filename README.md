# Google Business Profile SEO Automation

Automação profissional em Python para geração de conteúdo SEO para Google Meu Negócio, com interface web SaaS.

## Funcionalidades

- Leitura de empresas a partir de arquivo CSV
- Geração automática de descrições SEO otimizadas (via OpenAI)
- Criação de FAQs relevantes para cada negócio
- Geração de posts para Google Business Profile
- Exportação de todos os conteúdos gerados para CSV
- Interface web moderna com dashboard, upload, resultados e histórico
- Geração individual ou em lote

## Estrutura do Projeto

```
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py          # Servidor FastAPI
│   │   ├── routers/api.py   # Endpoints da API
│   │   ├── schemas.py       # Schemas Pydantic
│   │   └── seo/             # Módulo de automação SEO
│   ├── data/
│   ├── requirements.txt
│   └── render.yaml          # Config para deploy no Render
├── frontend/                # Interface React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/           # Páginas do app
│   │   ├── components/      # Componentes (shadcn/ui)
│   │   └── lib/api.js       # Cliente HTTP
│   ├── netlify.toml         # Config para deploy no Netlify
│   └── package.json
├── src/                     # CLI original
├── main.py                  # CLI original
├── tests/                   # Testes unitários
└── README.md
```

## Execução Local

### 1. Backend (API)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # Edite com sua OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

A API ficará em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

### 2. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

O frontend será aberto em `http://localhost:5173` e fará proxy das requisições `/api` para o backend.

> **Importante:** Inicie o backend primeiro, depois o frontend.

### 3. CLI Original

```bash
pip install -r requirements.txt
python main.py --create-sample   # Cria CSV de exemplo
python main.py                   # Executa automação
```

## Formato do CSV de Entrada

| Coluna | Descrição | Obrigatório |
|--------|-----------|-------------|
| `nome_empresa` | Nome da empresa | Sim |
| `segmento` | Segmento de atuação | Sim |
| `cidade` | Cidade onde atua | Sim |
| `diferenciais` | Diferenciais da empresa | Não |
| `publico_alvo` | Público-alvo | Não |

## API Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/health` | Health check |
| POST | `/api/upload-csv` | Upload de CSV |
| GET | `/api/uploaded-files` | Lista arquivos enviados |
| POST | `/api/preview-csv` | Pré-visualiza CSV |
| POST | `/api/generate` | Gera conteúdo individual |
| POST | `/api/generate-all` | Gera conteúdo em lote |
| GET | `/api/download/{file}` | Download de CSV |
| GET | `/api/history` | Histórico de gerações |
| GET/POST | `/api/settings` | Configurações da API |

## Deploy

### Frontend → Netlify

Conecte o repositório no Netlify e configure:
- **Build command:** `cd frontend && npm install && npm run build`
- **Publish directory:** `frontend/dist`
- **Redirects:** já configurados no `netlify.toml`

### Backend → Render

1. Crie um Web Service no Render
2. **Build Command:** `pip install -r backend/requirements.txt`
3. **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Adicione a variável de ambiente `OPENAI_API_KEY`
5. Atualize o `netlify.toml` com a URL do seu Render

## Licença

MIT
