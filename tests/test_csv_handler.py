import pandas as pd
import tempfile
from pathlib import Path

from src.csv_handler import CSVHandler
from src.models import Business


class TestCSVHandler:
    def test_read_businesses_valid_csv(self):
        csv_content = (
            "nome_empresa,segmento,cidade,diferenciais,publico_alvo\n"
            "Padaria Doce Sabor,Panificadora,São Paulo,Produtos artesanais,Famílias\n"
            "Clínica Sorriso,Odontologia,Rio de Janeiro,Tecnologia de ponta,Todas as idades\n"
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            tmp_path = Path(f.name)

        try:
            businesses = CSVHandler.read_businesses(tmp_path)
            assert len(businesses) == 2
            assert businesses[0].nome_empresa == "Padaria Doce Sabor"
            assert businesses[1].cidade == "Rio de Janeiro"
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_read_businesses_missing_required_column(self):
        csv_content = "nome_empresa,segmento\nPadaria,Panificadora\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            tmp_path = Path(f.name)

        try:
            import pytest
            with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
                CSVHandler.read_businesses(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_read_businesses_file_not_found(self):
        import pytest
        with pytest.raises(FileNotFoundError):
            CSVHandler.read_businesses(Path("arquivo_inexistente.csv"))

    def test_save_results(self):
        businesses = [
            Business(nome_empresa="Loja A", segmento="Varejo", cidade="SP",
                     descricao_seo="Descrição A", faqs="FAQ A", posts_gbp="Post A"),
            Business(nome_empresa="Loja B", segmento="Varejo", cidade="RJ",
                     descricao_seo="Descrição B", faqs="FAQ B", posts_gbp="Post B"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.csv"
            CSVHandler.save_results(businesses, output_path)

            assert output_path.exists()
            df = pd.read_csv(output_path)
            assert len(df) == 2
            assert list(df.columns) == [
                "nome_empresa", "segmento", "cidade",
                "diferenciais", "publico_alvo",
                "descricao_seo", "faqs", "posts_gbp"
            ]
            assert df.iloc[0]["descricao_seo"] == "Descrição A"

    def test_create_sample_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "sample.csv"
            CSVHandler.create_sample_file(output_path)

            assert output_path.exists()
            df = pd.read_csv(output_path)
            assert len(df) == 5
            assert list(df.columns) == [
                "nome_empresa", "segmento", "cidade",
                "diferenciais", "publico_alvo"
            ]
