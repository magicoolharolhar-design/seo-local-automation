import os
from pathlib import Path

from src.config import Config


class TestConfig:
    def test_base_dir_points_to_project_root(self):
        assert (Config.BASE_DIR / "main.py").exists()
        assert (Config.BASE_DIR / "src").is_dir()

    def test_data_directories(self):
        assert Config.DATA_DIR == Config.BASE_DIR / "data"
        assert Config.INPUT_DIR == Config.DATA_DIR / "input"
        assert Config.OUTPUT_DIR == Config.DATA_DIR / "output"

    def test_default_files(self):
        assert Config.DEFAULT_INPUT_FILE == Config.INPUT_DIR / "empresas.csv"
        assert Config.DEFAULT_OUTPUT_FILE == Config.OUTPUT_DIR / "generated_content.csv"

    def test_default_model(self):
        assert Config.OPENAI_MODEL == "gpt-4o-mini"

    def test_default_language(self):
        assert Config.CONTENT_LANGUAGE == "pt-BR"

    def test_validate_raises_without_key(self):
        old_key = Config.OPENAI_API_KEY
        Config.OPENAI_API_KEY = "sua_api_key_aqui"
        try:
            import pytest
            with pytest.raises(ValueError, match="OPENAI_API_KEY não configurada"):
                Config.validate()
        finally:
            Config.OPENAI_API_KEY = old_key

    def test_validate_success_with_valid_key(self):
        old_key = Config.OPENAI_API_KEY
        Config.OPENAI_API_KEY = "sk-real-key-12345"
        try:
            assert Config.validate() is True
        finally:
            Config.OPENAI_API_KEY = old_key

    def test_ensure_directories_creates_folders(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            input_dir = base / "input"
            output_dir = base / "output"

            input_dir.mkdir(parents=True, exist_ok=True)
            output_dir.mkdir(parents=True, exist_ok=True)

            assert input_dir.exists()
            assert output_dir.exists()
