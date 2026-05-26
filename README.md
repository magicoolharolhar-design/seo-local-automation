# Google Business Profile SEO Automation

Automação profissional em Python para geração de conteúdo SEO para Google Meu Negócio.

## Funcionalidades

- Leitura de empresas a partir de arquivo CSV
- Geração automática de descrições SEO otimizadas
- Criação de FAQs relevantes para cada negócio
- Geração de posts para Google Business Profile
- Exportação de todos os conteúdos gerados para CSV

## Requisitos

- Python 3.8+
- pandas
- openai
- python-dotenv

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure suas variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Adicione sua API Key da OpenAI

## Uso

1. Prepare seu arquivo CSV com as informações das empresas (veja `data/input/example_input.csv`)
2. Execute a automação:
```bash
python main.py
```

3. Os resultados serão exportados para `data/output/generated_content.csv`

## Estrutura do Projeto

```
├── src/
│   ├── __init__.py
│   ├── config.py          # Configurações do projeto
│   ├── csv_handler.py     # Leitura e escrita de CSV
│   ├── content_generator.py # Geração de conteúdo com IA
│   └── models.py          # Modelos de dados
├── data/
│   ├── input/             # CSVs de entrada
│   └── output/            # CSVs de saída
├── .env                   # Variáveis de ambiente
├── .env.example           # Exemplo de variáveis de ambiente
├── main.py                # Ponto de entrada principal
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

## Formato do CSV de Entrada

O arquivo CSV deve conter as seguintes colunas:
- `nome_empresa`: Nome da empresa
- `segmento`: Segmento de atuação
- `cidade`: Cidade onde atua
- `diferenciais`: Diferenciais da empresa (opcional)
- `publico_alvo`: Público-alvo (opcional)

## Licença

MIT
