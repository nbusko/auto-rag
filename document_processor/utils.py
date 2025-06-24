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
import logging
from config.app_settings import AppConfig

logger = logging.getLogger(__name__)
app_config = AppConfig()


async def process_file(byte_data):
    estimator_dict = {
        "pdf": process_pdf,
        "docx": process_docx,
        "doc": process_doc,
        "txt": process_txt,
        "xlsx": process_xlsx,
        "image": process_image,
    }
    file_type = await detect_file_type(byte_data)
    if file_type == "unknown":
        logger.warning("Unknown file type detected")
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
        "image/tiff": "image",
    }
    detected_type = mime_types.get(mime.from_buffer(byte_data), "unknown")
    logger.info(f"Detected file type: {detected_type}")
    return detected_type


async def extract_text_from_docx(docx_bytes):
    doc = Document(BytesIO(docx_bytes))
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return "\n".join(full_text)


async def extract_text_from_doc(doc_bytes):
    result = mammoth.extract_raw_text(BytesIO(doc_bytes))
    return result.value


async def process_text(text, max_length=3000):
    parts = []
    current_part = []
    current_length = 0

    for word in re.split(r"(\s+|\W)", text):
        if current_length + len(word) > max_length:
            parts.append("".join(current_part))
            current_part = []
            current_length = 0
        current_part.append(word)
        current_length += len(word)
    if current_part:
        parts.append("".join(current_part))
    return parts


async def process_doc(byte_data):
    text = await extract_text_from_doc(byte_data)
    return await process_text(text)


async def process_docx(byte_data):
    text = await extract_text_from_docx(byte_data)
    return await process_text(text)


async def process_txt(byte_data):
    text = byte_data.decode("utf-8")
    return await process_text(text)


async def process_xlsx(byte_data, max_length=8000):
    file_stream = BytesIO(byte_data)
    df = pd.read_excel(file_stream)

    rows = []
    for _, row in df.iterrows():

        row_text = " | ".join([str(val) for val in row.values if pd.notna(val)])
        rows.append(row_text)

    logger.info(f"Processed Excel file with {len(rows)} rows")
    return rows


async def process_pdf(byte_data):
    # Конвертируем PDF в изображения
    pdf_imgs = convert_from_bytes(byte_data)
    texts = []

    for i, img in enumerate(pdf_imgs):
        logger.info(f"Processing PDF page {i+1}/{len(pdf_imgs)}")

        # Масштабируем изображение, если оно слишком большое
        max_height = 720
        width, height = img.size
        if height > max_height:
            ratio = max_height / float(height)
            new_width = int(width * ratio)
            img = img.resize((new_width, max_height), Image.LANCZOS)

        # OCR
        text = await extract_text_from_image(img)
        texts.append(text)

    # Объединяем тексты
    full_text = " ".join(texts)

    return await process_text(full_text)


async def process_image(byte_data):
    image = Image.open(BytesIO(byte_data))
    if image.mode in ("RGBA", "P", "LA"):
        image = image.convert("RGB")

    # Извлекаем текст из изображения с помощью OCR
    text = await extract_text_from_image(image)

    return await process_text(text)


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
            api_key=app_config.OPENAI_API_KEY, base_url=str(app_config.OPENAI_BASE_URL)
        )

        response = client.chat.completions.create(
            model=app_config.OCR_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Ты OCR модель. Извлеки весь текст из этого изображения. Верни только текст без дополнительных комментариев.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error during OCR: {e}")
        return ""
