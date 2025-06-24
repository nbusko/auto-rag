import magic
import re
from docx import Document
import mammoth
from io import BytesIO
import pandas as pd
from pdf2image import convert_from_bytes
import base64
from PIL import Image
import openai
from app.config import settings

async def process_file(byte_data):
    estimator_dict = {
        "pdf": process_pdf,
        "docx": process_docx,
        "doc": process_doc,
        "txt": process_txt,
        "xlsx": process_xlsx,
        "image": process_image
    }
    file_type = await detect_file_type(byte_data)
    if file_type == "unknown":
        return "txt", ["unknown"]
    estimator = estimator_dict[file_type]
    data = await estimator(byte_data)

    return file_type, data

async def detect_file_type(byte_data):
    mime = magic.Magic(mime=True)
    mime_types = {
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/msword": "doc",
        "text/plain": "txt",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "image/jpeg": "image",
        "image/png": "image",
        "image/gif": "image",
        "image/bmp": "image",
        "image/tiff": "image"
    }
    return mime_types.get(mime.from_buffer(byte_data), "unknown")

async def extract_text_from_docx(docx_bytes):
    doc = Document(BytesIO(docx_bytes))
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

async def extract_text_from_doc(doc_bytes):
    result = mammoth.extract_raw_text(BytesIO(doc_bytes))
    return result.value

async def process_text(text, max_length=3000):
    parts = []
    current_part = []
    current_length = 0

    for word in re.split(r'(\s+|\W)', text):
        if current_length + len(word) > max_length:
            parts.append(''.join(current_part))
            current_part = []
            current_length = 0
        current_part.append(word)
        current_length += len(word)
    if current_part:
        parts.append(''.join(current_part))
    return parts

async def process_doc(byte_data):
    text = await extract_text_from_doc(byte_data)
    # Конвертируем в markdown
    markdown_text = await convert_to_markdown(text)
    return await process_text(markdown_text)

async def process_docx(byte_data):
    text = await extract_text_from_docx(byte_data)
    # Конвертируем в markdown
    markdown_text = await convert_to_markdown(text)
    return await process_text(markdown_text)

async def process_txt(byte_data):
    text = byte_data.decode('utf-8')
    # Конвертируем в markdown
    markdown_text = await convert_to_markdown(text)
    return await process_text(markdown_text)

async def process_xlsx(byte_data, max_length = 8000):
    file_stream = BytesIO(byte_data)
    df = pd.read_excel(file_stream)
    
    # Конвертируем таблицу в строки с конкатенированными столбцами
    rows = []
    for _, row in df.iterrows():
        # Объединяем все значения в строке
        row_text = " | ".join([str(val) for val in row.values if pd.notna(val)])
        rows.append(row_text)
    
    return rows

async def process_pdf(byte_data):
    # Конвертируем PDF в изображения
    pdf_imgs = convert_from_bytes(byte_data)
    
    # Извлекаем текст из каждого изображения с помощью OCR
    texts = []
    for img in pdf_imgs:
        text = await extract_text_from_image(img)
        texts.append(text)
    
    # Объединяем все тексты и конвертируем в markdown
    full_text = " ".join(texts)
    markdown_text = await convert_to_markdown(full_text)
    
    return await process_text(markdown_text)

async def process_image(byte_data):
    image = Image.open(BytesIO(byte_data))
    if image.mode in ('RGBA', 'P', 'LA'):
        image = image.convert('RGB')
    
    # Извлекаем текст из изображения с помощью OCR
    text = await extract_text_from_image(image)
    
    # Конвертируем в markdown
    markdown_text = await convert_to_markdown(text)
    
    return await process_text(markdown_text)

async def extract_text_from_image(image):
    """
    Извлекает текст из изображения с помощью OCR
    """
    try:
        # Конвертируем изображение в base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Используем OpenAI Vision API для OCR
        client = openai.OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Извлеки весь текст из этого изображения. Верни только текст без дополнительных комментариев."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Ошибка при OCR: {e}")
        return ""

async def convert_to_markdown(text):
    """
    Конвертирует обычный текст в markdown формат с помощью LLM
    """
    try:
        client = openai.OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        
        prompt = f"""
        Конвертируй следующий текст в markdown формат. Сохрани структуру и смысл, но добавь соответствующее форматирование:
        - Заголовки для разделов
        - Списки где это уместно
        - Выделение важного текста
        - Таблицы если есть табличные данные
        
        Текст:
        {text}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.1
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Ошибка при конвертации в markdown: {e}")
        return text