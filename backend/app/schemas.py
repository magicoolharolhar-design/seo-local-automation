from pydantic import BaseModel
from typing import Optional


class GenerateRequest(BaseModel):
    nome_empresa: str
    segmento: str
    cidade: str
    diferenciais: Optional[str] = None
    publico_alvo: Optional[str] = None


class GenerateResponse(BaseModel):
    nome_empresa: str
    descricao_seo: str
    faqs: str
    posts_gbp: str


class SettingsUpdate(BaseModel):
    openai_api_key: str
    openai_model: Optional[str] = "gpt-4o-mini"
    content_language: Optional[str] = "pt-BR"
