"""
Modelos de dados do projeto.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Business:
    """Modelo de dados para uma empresa."""
    
    nome_empresa: str
    segmento: str
    cidade: str
    diferenciais: Optional[str] = None
    publico_alvo: Optional[str] = None
    
    # Campos gerados pela automação
    descricao_seo: Optional[str] = None
    faqs: Optional[str] = None
    posts_gbp: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Converte o modelo para dicionário."""
        return {
            'nome_empresa': self.nome_empresa,
            'segmento': self.segmento,
            'cidade': self.cidade,
            'diferenciais': self.diferenciais or '',
            'publico_alvo': self.publico_alvo or '',
            'descricao_seo': self.descricao_seo or '',
            'faqs': self.faqs or '',
            'posts_gbp': self.posts_gbp or '',
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Business':
        """Cria uma instância a partir de um dicionário."""
        return cls(
            nome_empresa=data.get('nome_empresa', ''),
            segmento=data.get('segmento', ''),
            cidade=data.get('cidade', ''),
            diferenciais=data.get('diferenciais'),
            publico_alvo=data.get('publico_alvo'),
        )
