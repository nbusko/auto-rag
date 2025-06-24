import uuid
import re
from typing import List, Tuple
import openai
from app.config import settings
from app.utils import process_file


class DocumentProcessor:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
    
    async def process_document(
        self, 
        file_binary: bytes, 
        document_id: uuid.UUID,
        split_method: str,
        batch_size: int
    ) -> Tuple[List[str], List[List[float]]]:
        """
        Обрабатывает документ и возвращает фрагменты текста с эмбеддингами
        """
        # Определяем тип файла и извлекаем содержимое
        file_type, data = await process_file(file_binary)
        
        # Обрабатываем в зависимости от типа файла
        if file_type == "xlsx":
            # Для таблиц - разбиваем по строкам
            texts = await self._process_table(data)
        else:
            # Для остальных документов - применяем выбранный метод разделения
            if split_method == "llm":
                texts = await self._split_by_llm(data)
            else:  # batch
                texts = await self._split_by_batch(data, batch_size)
        
        # Получаем эмбеддинги для всех фрагментов
        embeddings = await self._get_embeddings(texts)
        
        return texts, embeddings
    
    async def _process_table(self, data: List[str]) -> List[str]:
        """
        Обрабатывает таблицу - разбивает по строкам
        """
        # data содержит строки таблицы в виде конкатенированных столбцов
        return data
    
    async def _split_by_llm(self, data: List[str]) -> List[str]:
        """
        Разделяет документ на смысловые части с помощью LLM
        """
        # Объединяем все части документа
        full_text = " ".join(data)
        
        # Используем LLM для разделения на смысловые части
        prompt = f"""
        Раздели следующий текст на логические части. Каждая часть должна быть самодостаточной и содержать связанную информацию.
        Верни только текст, разделенный на части, без дополнительных комментариев.
        
        Текст:
        {full_text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            # Разделяем результат на части (предполагаем, что LLM разделил текст)
            parts = [part.strip() for part in result.split('\n\n') if part.strip()]
            
            # Если LLM не разделил текст, используем простое разделение
            if len(parts) <= 1:
                parts = await self._simple_split(full_text)
            
            return parts
            
        except Exception as e:
            print(f"Ошибка при разделении LLM: {e}")
            # Fallback к простому разделению
            return await self._simple_split(" ".join(data))
    
    async def _split_by_batch(self, data: List[str], batch_size: int) -> List[str]:
        """
        Разделяет документ на части по размеру
        """
        full_text = " ".join(data)
        return await self._simple_split(full_text, batch_size)
    
    async def _simple_split(self, text: str, max_length: int = 1000) -> List[str]:
        """
        Простое разделение текста по размеру
        """
        parts = []
        current_part = []
        current_length = 0
        
        # Разделяем по предложениям для лучшего качества
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for sentence in sentences:
            if current_length + len(sentence) > max_length and current_part:
                parts.append(" ".join(current_part))
                current_part = []
                current_length = 0
            
            current_part.append(sentence)
            current_length += len(sentence)
        
        if current_part:
            parts.append(" ".join(current_part))
        
        return parts
    
    async def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Получает эмбеддинги для списка текстов
        """
        try:
            response = self.client.embeddings.create(
                model=settings.embedder_model,
                input=texts
            )
            
            return [embedding.embedding for embedding in response.data]
            
        except Exception as e:
            print(f"Ошибка при получении эмбеддингов: {e}")
            # Возвращаем пустые эмбеддинги в случае ошибки
            return [[0.0] * 1536 for _ in texts]  # 1536 - размерность для text-embedding-3-small 