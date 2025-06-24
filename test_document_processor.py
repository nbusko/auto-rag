import requests
import uuid
import os

API_URL = "http://localhost:8000/api/v1/documents/process"

# Пример тестовых файлов (заменить на свои пути)
TEST_FILES = [
    ("test_doc.docx", "batch"),
    ("test_text.txt", "llm"),
    # ("test_table.xlsx", "batch"),
    # ("test_pdf.pdf", "batch"),
]


def test_document_processor(
    file_path,
    split_method="batch",
    batch_size=1000,
    llm_model="gpt-4o-mini",
    temperature=0.1,
):
    document_id = str(uuid.uuid4())
    with open(file_path, "rb") as f:
        files = {"document": (os.path.basename(file_path), f)}
        data = {
            "document_id": document_id,
            "split_method": split_method,
            "batch_size": batch_size,
            "llm_model": llm_model,
            "temperature": temperature,
            # "prompt_split": "",  # Можно указать кастомный промпт
            # "prompt_table": ""
        }
        print(f"\n--- Тестируем файл: {file_path} (split_method={split_method}) ---")
        response = requests.post(API_URL, files=files, data=data)
        print(f"Status code: {response.status_code}")
        try:
            resp_json = response.json()
        except Exception as e:
            print(f"Ошибка парсинга JSON: {e}\nОтвет: {response.text}")
            return
        print(f"Ответ: {resp_json}")
        if resp_json.get("status") == "success":
            print(
                f"\033[92mУспех! Чанков: {resp_json.get('chunks_count')}, Время: {resp_json.get('processing_time'):.2f} сек\033[0m"
            )
        else:
            print(f"\033[91mОшибка: {resp_json.get('message')}\033[0m")


def main():
    for file_path, split_method in TEST_FILES:
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден. Пропускаем.")
            continue
        test_document_processor(file_path, split_method=split_method)


if __name__ == "__main__":
    main()
