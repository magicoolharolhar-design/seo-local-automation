import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from src.models import Business


class TestMain:
    def test_create_sample_flag(self):
        test_args = ["main.py", "--create-sample"]
        with patch.object(sys, "argv", test_args):
            with tempfile.TemporaryDirectory() as tmpdir:
                with patch("src.config.Config.INPUT_DIR", Path(tmpdir) / "input"):
                    with patch("src.config.Config.OUTPUT_DIR", Path(tmpdir) / "output"):
                        import importlib
                        import src.csv_handler
                        original_create = src.csv_handler.CSVHandler.create_sample_file

                        called = False
                        def fake_create(path):
                            nonlocal called
                            called = True
                            path.parent.mkdir(parents=True, exist_ok=True)
                            path.write_text("fake", encoding="utf-8")

                        src.csv_handler.CSVHandler.create_sample_file = fake_create
                        try:
                            import main
                            main.main()
                            assert called, "create_sample_file should have been called"
                        finally:
                            src.csv_handler.CSVHandler.create_sample_file = original_create

    def test_missing_input_file_shows_hint(self):
        test_args = ["main.py", "-i", "nonexistent.csv"]
        with patch.object(sys, "argv", test_args):
            with tempfile.TemporaryDirectory() as tmpdir:
                with (
                    patch("src.config.Config.INPUT_DIR", Path(tmpdir) / "input"),
                    patch("src.config.Config.OUTPUT_DIR", Path(tmpdir) / "output"),
                    patch("src.config.Config.OPENAI_API_KEY", "sk-valid-key"),
                ):
                    import main
                    with patch("builtins.print") as mock_print:
                        main.main()
                        printed = "".join(
                            str(call) for call in mock_print.call_args_list
                        )
                        assert "não encontrado" in printed
                        assert "--create-sample" in printed

    def test_config_error_prints_message(self):
        test_args = ["main.py", "-i", "some.csv"]
        with patch.object(sys, "argv", test_args):
            with tempfile.TemporaryDirectory() as tmpdir:
                with (
                    patch("src.config.Config.INPUT_DIR", Path(tmpdir) / "input"),
                    patch("src.config.Config.OUTPUT_DIR", Path(tmpdir) / "output"),
                    patch("src.config.Config.validate", side_effect=ValueError("OPENAI_API_KEY não configurada")),
                ):
                    import main
                    with patch("builtins.print") as mock_print:
                        main.main()
                        printed = "".join(
                            str(call) for call in mock_print.call_args_list
                        )
                        assert "Erro de configuração" in printed
