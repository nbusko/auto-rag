import logging
import os

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/rag_service.log', encoding='utf-8')
        ]
    )
    

    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('fastapi').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.INFO)
    
 
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")