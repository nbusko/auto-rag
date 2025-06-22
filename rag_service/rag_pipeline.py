import os
import uuid
import logging
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        logger.info("Initializing RAG Pipeline...")
        
        # Инициализируем модель для эмбеддингов
        logger.info("Loading embedding model: sergeyzh/rubert-mini-frida")
        self.embedding_model = SentenceTransformer('sergeyzh/rubert-mini-frida')
        
        # Инициализируем OpenAI клиент
        logger.info("Initializing OpenAI client")
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.proxyapi.ru/openai/v1")
        
        # Инициализируем LangChain модель
        logger.info("Initializing LangChain model")
        self.llm = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            base_url="https://api.proxyapi.ru/openai/v1"
        )
        
        # Шаблон промпта для RAG
        self.rag_prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            Ты - полезный ассистент, который отвечает на вопросы пользователя на основе предоставленного контекста.
            
            Контекст:
            {context}
            
            Вопрос: {question}
            
            Ответь на вопрос, используя только информацию из предоставленного контекста. 
            Если в контексте нет информации для ответа на вопрос, скажи об этом честно.
            Отвечай на русском языке.
            """
        )
        logger.info("RAG Pipeline initialized successfully")
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Получить эмбеддинг для запроса"""
        logger.info(f"Getting embedding for query: {query[:50]}...")
        try:
            embedding = self.embedding_model.encode(query, convert_to_tensor=False)
            logger.info("Query embedding generated successfully")
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise
    
    def retrieve_relevant_chunks(self, query: str, document_id: str, top_k: int, db_manager) -> List[dict]:
        """Получить релевантные чанки для запроса"""
        logger.info(f"Retrieving relevant chunks for document_id: {document_id}, top_k: {top_k}")
        try:
            # Получаем эмбеддинг запроса
            query_embedding = self.get_query_embedding(query)
            
            # Ищем похожие чанки
            similar_chunks = db_manager.search_similar_chunks(
                query_embedding=query_embedding,
                document_id=document_id,
                top_k=top_k
            )
            
            logger.info(f"Retrieved {len(similar_chunks)} relevant chunks")
            return similar_chunks
        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {e}")
            return []
    
    def generate_response(self, query: str, context_chunks: List[dict]) -> str:
        """Генерировать ответ на основе контекста"""
        logger.info(f"Generating response for query: {query[:50]}...")
        try:
            if not context_chunks:
                logger.warning("No context chunks provided for response generation")
                return "Извините, не удалось найти релевантную информацию для ответа на ваш вопрос."
            
            # Формируем контекст из найденных чанков
            context = "\n\n".join([chunk["content"] for chunk in context_chunks])
            logger.info(f"Context length: {len(context)} characters")
            
            # Формируем промпт
            prompt = self.rag_prompt_template.format(context=context, question=query)
            
            # Генерируем ответ
            messages = [
                SystemMessage(content="Ты - полезный ассистент, который отвечает на вопросы на основе предоставленного контекста."),
                HumanMessage(content=prompt)
            ]
            
            logger.info("Sending request to LLM")
            response = self.llm.invoke(messages)
            logger.info("Response generated successfully")
            return response.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Ошибка при генерации ответа: {str(e)}"
    
    def process_rag_request(self, chat_id: str, user_message: str, db_manager) -> dict:
        """Обработать RAG запрос"""
        logger.info(f"Processing RAG request for chat_id: {chat_id}")
        try:
            # Получаем параметры чата
            params = db_manager.get_chat_params(chat_id)
            if not params:
                logger.error(f"Chat parameters not found for chat_id: {chat_id}")
                return {
                    "error": "Параметры чата не найдены. Установите параметры перед использованием RAG."
                }
            
            logger.info(f"Retrieved chat params: document_id={params.get('document_id')}, top_k={params.get('top_k')}")
            
            # Получаем релевантные чанки
            relevant_chunks = self.retrieve_relevant_chunks(
                query=user_message,
                document_id=params["document_id"],
                top_k=params["top_k"],
                db_manager=db_manager
            )
            
            # Генерируем ответ
            assistant_message = self.generate_response(user_message, relevant_chunks)
            
            # Генерируем ID для сообщения
            message_id = str(uuid.uuid4())
            
            # Сохраняем сообщения в базу
            logger.info("Saving messages to database")
            db_manager.add_message(chat_id, message_id, "user", user_message)
            db_manager.add_message(chat_id, str(uuid.uuid4()), "assistant", assistant_message)
            
            logger.info(f"RAG request processed successfully for chat_id: {chat_id}")
            
            return {
                "chat_id": chat_id,
                "message_id": message_id,
                "assistant_message": assistant_message,
                "retrieved_chunks": relevant_chunks,
                "similarity_scores": [chunk["similarity"] for chunk in relevant_chunks]
            }
        except Exception as e:
            logger.error(f"Error processing RAG request for chat_id {chat_id}: {e}", exc_info=True)
            return {
                "error": f"Ошибка при обработке RAG запроса: {str(e)}"
            } 