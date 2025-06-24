import faiss
import numpy as np
from typing import List


class EmbeddingSearcher:
    def __init__(self, embeddings: List[List[float]], texts: List[str]):
        """
        embeddings: нормализованные эмбеддинги (L2-норма == 1), размерность 312
        texts: соответствующие тексты
        """
        self.embeddings = np.array(embeddings).astype("float32")
        self.texts = texts

        assert self.embeddings.shape[0] == len(
            self.texts
        ), "Число эмбеддингов и текстов должно совпадать"
        assert (
            self.embeddings.shape[1] == 312
        ), "Размерность эмбеддингов должна быть 312"

        self.index = self._build_index(self.embeddings)

    def _build_index(self, embeddings: np.ndarray):
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        return index

    def search(
        self, query_embedding: List[float], top_k: int, threshold: float
    ) -> List[str]:
        """
        Выполняет поиск по cosine similarity (dot product).

        query_embedding: нормализованный эмбеддинг запроса
        top_k: сколько вернуть ближайших соседей
        threshold: минимальное значение cosine similarity
        """
        query = np.array([query_embedding], dtype="float32")  # (1, 312)

        similarities, indices = self.index.search(query, top_k)

        results = []
        for idx, sim in zip(indices[0], similarities[0]):
            if sim >= threshold and idx != -1:
                results.append(self.texts[idx])

        return results
