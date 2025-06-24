import logging
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from config.contracts import DocumentResponse, SplitMethod
from document_pipeline import DocumentPipeline

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Document Processor Service is running", "docs": "/docs"}

@router.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "timestamp": datetime.now()}

@router.post("/documents/process", response_model=DocumentResponse)
async def process_document(
    document_id: str = Form(),
    document: UploadFile = File(),
    split_method: str = Form(default="batch"),
    batch_size: int = Form(default=1000),
    llm_model: str = Form(default="gpt-4o-mini"),
    temperature: float = Form(default=0.1),
    prompt_split: str = Form(default=""),
    prompt_table: str = Form(default="")
):
    """
    Обрабатывает документ и возвращает фрагменты текста с эмбеддингами
    
    Args:
        document_id: UUID документа
        document: Загружаемый файл
        split_method: Метод разделения ("llm" или "batch")
        batch_size: Размер батча (игнорируется для "llm" и таблиц)
        llm_model: Модель LLM для разделения
        temperature: Температура для LLM
        prompt_split: Кастомный промпт для разделения
        prompt_table: Кастомный промпт для таблиц
    
    Returns:
        DocumentResponse с фрагментами текста и эмбеддингами
    """
    try:
        logger.info(f"Processing document request for document_id: {document_id}")
        
        # Валидируем document_id
        try:
            doc_uuid = uuid.UUID(document_id)
        except ValueError:
            logger.error(f"Invalid document_id format: {document_id}")
            raise HTTPException(
                status_code=400,
                detail="Invalid document_id format. Must be a valid UUID."
            )
        
        # Валидируем split_method
        try:
            split_enum = SplitMethod(split_method)
        except ValueError:
            logger.error(f"Invalid split_method: {split_method}")
            raise HTTPException(
                status_code=400,
                detail="split_method must be either 'llm' or 'batch'"
            )
        
        # Валидируем batch_size
        if batch_size <= 0:
            logger.error(f"Invalid batch_size: {batch_size}")
            raise HTTPException(
                status_code=400,
                detail="batch_size must be positive"
            )
        
        # Валидируем temperature
        if not 0.0 <= temperature <= 1.0:
            logger.error(f"Invalid temperature: {temperature}")
            raise HTTPException(
                status_code=400,
                detail="temperature must be between 0.0 and 1.0"
            )
        
        # Читаем файл
        logger.info(f"Reading file: {document.filename}")
        file_binary = await document.read()
        
        if not file_binary:
            logger.error("Empty file received")
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )
        
        # Обрабатываем документ
        logger.info(f"Starting document processing with method: {split_method}")
        document_pipeline = DocumentPipeline()
        
        result = await document_pipeline.process_document(
            file_binary=file_binary,
            document_id=doc_uuid,
            split_method=split_enum,
            batch_size=batch_size,
            llm_model=llm_model,
            temperature=temperature,
            prompt_split=prompt_split,
            prompt_table=prompt_table
        )
        
        # Проверяем результат
        if result.status == "error":
            logger.error(f"Document processing failed: {result.message}")
            return result
        
        logger.info(f"Document processing completed successfully for document_id: {document_id}")
        logger.info(f"Created {result.chunks_count} chunks in {result.processing_time:.2f}s")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}") 