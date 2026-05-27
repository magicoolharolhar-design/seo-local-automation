"""
Geração de conteúdo usando IA.
"""

from openai import OpenAI
from typing import Optional

from .config import Config
from .models import Business


class ContentGenerator:
    """Classe para geração de conteúdo SEO usando OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o gerador de conteúdo.
        
        Args:
            api_key: Chave da API OpenAI. Se None, usa a do Config.
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.language = Config.CONTENT_LANGUAGE
        
        self.client = OpenAI(api_key=self.api_key)
    
    def _build_prompt(self, business: Business, content_type: str) -> str:
        """
        Constrói o prompt para geração de conteúdo.
        
        Args:
            business: Objeto Business com dados da empresa.
            content_type: Tipo de conteúdo a ser gerado.
            
        Returns:
            Prompt formatado para a IA.
        """
        base_info = (
            f"Empresa: {business.nome_empresa}\n"
            f"Segmento: {business.segmento}\n"
            f"Cidade: {business.cidade}"
        )
        
        if business.diferenciais:
            base_info += f"\nDiferenciais: {business.diferenciais}"
        
        if business.publico_alvo:
            base_info += f"\nPúblico-alvo: {business.publico_alvo}"
        
        prompts = {
            'descricao': (
                f"Com base nas informações abaixo, crie uma descrição SEO otimizada "
                f"para Google Meu Negócio (até 750 caracteres).\n\n"
                f"{base_info}\n\n"
                f"Requisitos:\n"
                f"- Use palavras-chave relevantes para o segmento e localização\n"
                f"- Destaque os diferenciais da empresa\n"
                f"- Seja persuasivo e convidativo\n"
                f"- Inclua call-to-action\n"
                f"- Escreva em {self.language}\n"
                f"- Formato: texto corrido, sem markdown"
            ),
            'faqs': (
                f"Com base nas informações abaixo, crie 5 FAQs (Perguntas Frequentes) "
                f"relevantes para Google Meu Negócio.\n\n"
                f"{base_info}\n\n"
                f"Requisitos:\n"
                f"- Crie perguntas que clientes reais fariam\n"
                f"- Forneça respostas úteis e informativas\n"
                f"- Cubra tópicos como: horários, serviços, preços, localização\n"
                f"- Escreva em {self.language}\n"
                f"- Formato: Cada FAQ no formato 'P: [pergunta]\\nR: [resposta]'"
            ),
            'posts': (
                f"Com base nas informações abaixo, crie 3 posts para Google Business Profile.\n\n"
                f"{base_info}\n\n"
                f"Requisitos:\n"
                f"- Posts variados: promocional, informativo e engajamento\n"
                f"- Máximo de 1500 caracteres por post\n"
                f"- Use emojis de forma moderada\n"
                f"- Inclua hashtags relevantes\n"
                f"- Escreva em {self.language}\n"
                f"- Formato: 'POST 1:', 'POST 2:', 'POST 3:' separados por linhas em branco"
            )
        }
        
        return prompts.get(content_type, '')
    
    def generate_description(self, business: Business) -> str:
        """
        Gera descrição SEO para uma empresa.
        
        Args:
            business: Objeto Business com dados da empresa.
            
        Returns:
            Descrição SEO gerada.
        """
        prompt = self._build_prompt(business, 'descricao')
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Você é um especialista em SEO Local e Google Meu Negócio."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_faqs(self, business: Business) -> str:
        """
        Gera FAQs para uma empresa.
        
        Args:
            business: Objeto Business com dados da empresa.
            
        Returns:
            FAQs geradas.
        """
        prompt = self._build_prompt(business, 'faqs')
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Você é um especialista em SEO Local e Google Meu Negócio."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_posts(self, business: Business) -> str:
        """
        Gera posts para Google Business Profile.
        
        Args:
            business: Objeto Business com dados da empresa.
            
        Returns:
            Posts gerados.
        """
        prompt = self._build_prompt(business, 'posts')
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Você é um especialista em SEO Local e Google Meu Negócio."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_all_content(self, business: Business) -> Business:
        """
        Gera todo o conteúdo para uma empresa.
        
        Args:
            business: Objeto Business com dados da empresa.
            
        Returns:
            Objeto Business com conteúdo gerado.
        """
        print(f"  📝 Gerando descrição para {business.nome_empresa}...")
        business.descricao_seo = self.generate_description(business)
        
        print(f"  ❓ Gerando FAQs para {business.nome_empresa}...")
        business.faqs = self.generate_faqs(business)
        
        print(f"  📱 Gerando posts para {business.nome_empresa}...")
        business.posts_gbp = self.generate_posts(business)
        
        return business
