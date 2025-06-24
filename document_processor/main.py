import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import router
from config.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Document Processor Service", 
    version="1.0.0",
    description="Сервис для обработки документов и создания эмбеддингов",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

logger.info("Document Processor Service initialized successfully")

@app.on_event("startup")
async def startup_event():
    logger.info("Document Processor Service starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Document Processor Service shutting down...")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Document Processor Service with uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
