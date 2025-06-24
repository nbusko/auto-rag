import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from app.models import DocumentResponse
from app.document_processor import DocumentProcessor

router = APIRouter(prefix="/documents", tags=["documents"])

# Создаем экземпляр процессора документов
document_processor = DocumentProcessor()


@router.post("/process", response_model=DocumentResponse)
async def process_document(
    document_id: str = Form(),
    document: UploadFile = File(),
    split: str = Form(default="batch"),
    batch_size: int = Form(default=1000)
):
    """
    Обрабатывает документ и возвращает фрагменты текста с эмбеддингами
    
    Args:
        document_id: UUID документа
        document: Загружаемый файл
        split: Метод разделения ("llm" или "batch")
        batch_size: Размер батча (игнорируется для "llm" и таблиц)
    
    Returns:
        DocumentResponse с фрагментами текста и эмбеддингами
    """
    try:
        # Валидируем document_id
        try:
            doc_uuid = uuid.UUID(document_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid document_id format. Must be a valid UUID."
            )
        
        # Валидируем split
        if split not in ["llm", "batch"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="split must be either 'llm' or 'batch'"
            )
        
        # Валидируем batch_size
        if batch_size <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="batch_size must be positive"
            )
        
        # Читаем файл
        file_binary = await document.read()
        
        # Обрабатываем документ
        texts, embeddings = await document_processor.process_document(
            file_binary=file_binary,
            document_id=doc_uuid,
            split_method=split,
            batch_size=batch_size
        )
        
        # Возвращаем результат
        return DocumentResponse(
            document_id=doc_uuid,
            texts=texts,
            embeddings=embeddings
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Проверка здоровья сервиса
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy", "service": "document-processor"}
    ) 