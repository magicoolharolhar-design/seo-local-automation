from unittest.mock import Mock, patch

import pytest

from src.content_generator import ContentGenerator
from src.models import Business


class TestContentGenerator:
    def setup_method(self):
        self.business = Business(
            nome_empresa="Padaria Doce Sabor",
            segmento="Panificadora e Confeitaria",
            cidade="São Paulo - SP",
            diferenciais="Produtos artesanais, entrega em domicílio",
            publico_alvo="Famílias e moradores do bairro"
        )

    @patch("src.content_generator.OpenAI")
    def test_generate_description(self, mock_openai):
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Descrição SEO da padaria."
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        generator = ContentGenerator(api_key="test-key")
        result = generator.generate_description(self.business)
        assert result == "Descrição SEO da padaria."

    @patch("src.content_generator.OpenAI")
    def test_generate_faqs(self, mock_openai):
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "P: Horários? R: 8h às 20h"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        generator = ContentGenerator(api_key="test-key")
        result = generator.generate_faqs(self.business)
        assert result == "P: Horários? R: 8h às 20h"

    @patch("src.content_generator.OpenAI")
    def test_generate_posts(self, mock_openai):
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "POST 1: Promoção imperdível!"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        generator = ContentGenerator(api_key="test-key")
        result = generator.generate_posts(self.business)
        assert result == "POST 1: Promoção imperdível!"

    @patch("src.content_generator.OpenAI")
    def test_generate_all_content(self, mock_openai):
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Conteúdo gerado"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        generator = ContentGenerator(api_key="test-key")
        result = generator.generate_all_content(self.business)

        assert result.descricao_seo == "Conteúdo gerado"
        assert result.faqs == "Conteúdo gerado"
        assert result.posts_gbp == "Conteúdo gerado"

    @patch("src.content_generator.OpenAI")
    def test_build_prompt_descricao(self, mock_openai):
        generator = ContentGenerator(api_key="test-key")
        prompt = generator._build_prompt(self.business, "descricao")
        assert "Padaria Doce Sabor" in prompt
        assert "descrição SEO otimizada" in prompt
        assert "Google Meu Negócio" in prompt

    @patch("src.content_generator.OpenAI")
    def test_build_prompt_faqs(self, mock_openai):
        generator = ContentGenerator(api_key="test-key")
        prompt = generator._build_prompt(self.business, "faqs")
        assert "5 FAQs" in prompt
        assert "Perguntas Frequentes" in prompt

    @patch("src.content_generator.OpenAI")
    def test_build_prompt_posts(self, mock_openai):
        generator = ContentGenerator(api_key="test-key")
        prompt = generator._build_prompt(self.business, "posts")
        assert "3 posts" in prompt
        assert "Google Business Profile" in prompt

    @patch("src.content_generator.OpenAI")
    def test_build_prompt_unknown_type(self, mock_openai):
        generator = ContentGenerator(api_key="test-key")
        prompt = generator._build_prompt(self.business, "unknown")
        assert prompt == ""

    @patch("src.content_generator.OpenAI")
    def test_generate_description_api_error(self, mock_openai):
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")

        generator = ContentGenerator(api_key="test-key")
        with pytest.raises(Exception, match="API Error"):
            generator.generate_description(self.business)
