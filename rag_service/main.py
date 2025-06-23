import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from datetime import datetime
import os

from models import RAGRequest, RAGResponse
from database import DatabaseManager
from rag_pipeline import RAGPipeline

from config.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Service", 
    version="1.0.0",
    description="Сервис для обработки RAG запросов и генерации ответов на основе контекста",
    docs_url="/docs",
    redoc_url=None,
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Initializing RAG Service...")
rag_pipeline = RAGPipeline()
logger.info("RAG Service initialized successfully")

@app.on_event("startup")
async def startup_event():
    logger.info("RAG Service starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("RAG Service shutting down...")


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting RAG Service with uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=5060, log_level="info") 