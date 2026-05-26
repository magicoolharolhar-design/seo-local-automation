"""
Configurações do projeto.
"""

import os
from dotenv import load_dotenv
from pathlib import Path


class Config:
    """Classe de configuração do projeto."""
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Diretório base do projeto
    BASE_DIR = Path(__file__).parent.parent
    
    # Diretórios de dados
    DATA_DIR = BASE_DIR / 'data'
    INPUT_DIR = DATA_DIR / 'input'
    OUTPUT_DIR = DATA_DIR / 'output'
    
    # Configurações da OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    CONTENT_LANGUAGE = os.getenv('CONTENT_LANGUAGE', 'pt-BR')
    
    # Arquivos padrão
    DEFAULT_INPUT_FILE = INPUT_DIR / 'empresas.csv'
    DEFAULT_OUTPUT_FILE = OUTPUT_DIR / 'generated_content.csv'
    
    @classmethod
    def validate(cls) -> bool:
        """Valida se as configurações necessárias estão presentes."""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == 'sua_api_key_aqui':
            raise ValueError(
                "OPENAI_API_KEY não configurada. "
                "Copie .env.example para .env e adicione sua API Key."
            )
        return True
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Garante que os diretórios necessários existam."""
        cls.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
