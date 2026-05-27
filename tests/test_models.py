from src.models import Business


class TestBusiness:
    def test_create_business_with_required_fields(self):
        b = Business(nome_empresa="Padaria Doce Sabor", segmento="Padaria", cidade="São Paulo")
        assert b.nome_empresa == "Padaria Doce Sabor"
        assert b.segmento == "Padaria"
        assert b.cidade == "São Paulo"
        assert b.diferenciais is None
        assert b.publico_alvo is None
        assert b.descricao_seo is None
        assert b.faqs is None
        assert b.posts_gbp is None

    def test_create_business_with_all_fields(self):
        b = Business(
            nome_empresa="Clínica Sorriso",
            segmento="Odontologia",
            cidade="RJ",
            diferenciais="Tecnologia de ponta",
            publico_alvo="Famílias",
            descricao_seo="Melhor clínica",
            faqs="P: Horários? R: 8h-18h",
            posts_gbp="Post 1..."
        )
        assert b.diferenciais == "Tecnologia de ponta"
        assert b.descricao_seo == "Melhor clínica"

    def test_to_dict(self):
        b = Business(nome_empresa="Loja X", segmento="Varejo", cidade="BH")
        data = b.to_dict()
        assert data["nome_empresa"] == "Loja X"
        assert data["descricao_seo"] == ""

    def test_to_dict_with_generated_content(self):
        b = Business(
            nome_empresa="Loja X",
            segmento="Varejo",
            cidade="BH",
            descricao_seo="Descrição SEO",
            faqs="FAQ 1",
            posts_gbp="Post 1"
        )
        data = b.to_dict()
        assert data["descricao_seo"] == "Descrição SEO"
        assert data["faqs"] == "FAQ 1"
        assert data["posts_gbp"] == "Post 1"

    def test_from_dict(self):
        data = {
            "nome_empresa": "Restaurante Sabor",
            "segmento": "Restaurante",
            "cidade": "Curitiba",
            "diferenciais": "Comida caseira",
            "publico_alvo": "Famílias"
        }
        b = Business.from_dict(data)
        assert b.nome_empresa == "Restaurante Sabor"
        assert b.diferenciais == "Comida caseira"

    def test_from_dict_missing_optional(self):
        data = {"nome_empresa": "Loja", "segmento": "Varejo", "cidade": "SP"}
        b = Business.from_dict(data)
        assert b.diferenciais is None
        assert b.publico_alvo is None
