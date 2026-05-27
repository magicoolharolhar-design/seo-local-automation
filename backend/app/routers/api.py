import os
import json
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ..schemas import GenerateRequest, GenerateResponse, SettingsUpdate
from ..seo.csv_handler import CSVHandler
from ..seo.content_generator import ContentGenerator
from ..seo.config import Config

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")
HISTORY_FILE = os.path.join(BASE_DIR, "data", "history.json")


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(entry: dict):
    history = load_history()
    history.insert(0, entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    return history


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Apenas arquivos CSV são aceitos.")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    return {"message": "Arquivo enviado com sucesso", "filename": file.filename}


@router.get("/uploaded-files")
async def list_uploaded_files():
    files = []
    for fname in os.listdir(UPLOAD_DIR):
        if fname.endswith(".csv") and fname != ".gitkeep":
            fpath = os.path.join(UPLOAD_DIR, fname)
            files.append({"name": fname, "size": os.path.getsize(fpath)})
    return {"files": files}


@router.post("/preview-csv")
async def preview_csv(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Arquivo não encontrado")
    try:
        from pathlib import Path
        businesses = CSVHandler.read_businesses(Path(file_path))
        data = [b.to_dict() for b in businesses]
        return {"businesses": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(400, str(e))


class GenerateAllRequest(BaseModel):
    filename: Optional[str] = None


@router.post("/generate")
async def generate_single(req: GenerateRequest):
    try:
        from pathlib import Path
        from ..seo.models import Business

        business = Business(
            nome_empresa=req.nome_empresa,
            segmento=req.segmento,
            cidade=req.cidade,
            diferenciais=req.diferenciais,
            publico_alvo=req.publico_alvo,
        )
        generator = ContentGenerator()
        generator.generate_all_content(business)

        return GenerateResponse(
            nome_empresa=business.nome_empresa,
            descricao_seo=business.descricao_seo or "",
            faqs=business.faqs or "",
            posts_gbp=business.posts_gbp or "",
        )
    except Exception as e:
        raise HTTPException(500, f"Erro ao gerar conteúdo: {str(e)}")


@router.post("/generate-all")
async def generate_all(req: GenerateAllRequest):
    filename = req.filename
    if not filename:
        files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".csv") and f != ".gitkeep"]
        if not files:
            raise HTTPException(400, "Nenhum arquivo CSV encontrado. Faça upload primeiro.")
        filename = sorted(files)[-1]

    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Arquivo não encontrado")

    try:
        from pathlib import Path
        businesses = CSVHandler.read_businesses(Path(file_path))
        total = len(businesses)
        generator = ContentGenerator()
        results = []
        for i, business in enumerate(businesses):
            generator.generate_all_content(business)
            results.append({
                "nome_empresa": business.nome_empresa,
                "descricao_seo": business.descricao_seo or "",
                "faqs": business.faqs or "",
                "posts_gbp": business.posts_gbp or "",
            })

        output_filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        CSVHandler.save_results(businesses, output_path)

        entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "total": total,
            "output": output_filename,
        }
        save_history(entry)

        return {
            "results": results,
            "total": total,
            "output_file": output_filename,
            "history_id": entry["id"],
        }
    except Exception as e:
        raise HTTPException(500, f"Erro ao processar: {str(e)}")


@router.get("/download/{filename}")
async def download(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Arquivo não encontrado")
    return FileResponse(file_path, media_type="text/csv", filename=filename)


@router.get("/history")
async def get_history():
    return {"history": load_history()}


@router.post("/settings")
async def update_settings(settings: SettingsUpdate):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    os.environ["OPENAI_MODEL"] = settings.openai_model
    os.environ["CONTENT_LANGUAGE"] = settings.content_language
    Config.OPENAI_API_KEY = settings.openai_api_key
    Config.OPENAI_MODEL = settings.openai_model
    Config.CONTENT_LANGUAGE = settings.content_language
    return {"message": "Configurações salvas com sucesso"}


@router.get("/settings")
async def get_settings():
    return {
        "openai_api_key": Config.OPENAI_API_KEY[:8] + "..." if Config.OPENAI_API_KEY else "",
        "openai_model": Config.OPENAI_MODEL,
        "content_language": Config.CONTENT_LANGUAGE,
    }
