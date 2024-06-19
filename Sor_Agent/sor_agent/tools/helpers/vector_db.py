# sor_agent/tools/helpers/vector_db.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorDB:
    def __init__(self):
        self.memory_vectors = {}
        self.memory_texts = {}

    def add_memory(self, key, vector, text):
        self.memory_vectors[key] = vector
        self.memory_texts[key] = text

    def get_similar_memory(self, vector, top_n=1):
        if not self.memory_vectors:
            return []
        vectors = np.array(list(self.memory_vectors.values()))
        keys = list(self.memory_vectors.keys())
        similarities = cosine_similarity([vector], vectors)[0]
        sorted_indices = np.argsort(similarities)[::-1][:top_n]
        return [(keys[i], similarities[i], self.memory_texts[keys[i]]) for i in sorted_indices]
