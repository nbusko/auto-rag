from pydantic import BaseSettings, Field
from constants import MAP_REDUCE_PROMPT, GENERATE_FINAL_ANSWER_PROMPT, RETRIEVE_PROMPT

class AppConfig(BaseSettings):
    # Промпты
    prompt_retrieve: str = Field(
        default=RETRIEVE_PROMPT,
        description="Промпт для retrieval-фазы"
    )
    prompt_augmentation: str = Field(
        default=MAP_REDUCE_PROMPT,
        description="Промпт для обогащения запроса"
    )
    prompt_generation: str = Field(
        default=GENERATE_FINAL_ANSWER_PROMPT,
        description="Промпт для генерации финального ответа"
    )

    # Параметры генерации
    top_k: int = Field(default=5, ge=1, description="Количество извлекаемых документов")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Температура генерации LLM")
    threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Порог близости документов")
    llm: str = Field(default="gpt-4o-mini", description="Наименование LLM по умолчанию")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
