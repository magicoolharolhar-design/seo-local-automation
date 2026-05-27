import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from .routers import api

load_dotenv()

app = FastAPI(
    title="SEO Local Automation API",
    description="API para geração de conteúdo SEO para Google Meu Negócio",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "output")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(os.path.join(UPLOAD_DIR, ".gitkeep")):
    open(os.path.join(UPLOAD_DIR, ".gitkeep"), "a").close()
if not os.path.exists(os.path.join(OUTPUT_DIR, ".gitkeep")):
    open(os.path.join(OUTPUT_DIR, ".gitkeep"), "a").close()
