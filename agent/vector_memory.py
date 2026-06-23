from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorMemory:
    def __init__(self):
        self.texts = []
        self.values = []
        self.vectorizer = TfidfVectorizer()
        self.vectors = None

    def add(self, text, value):
        self.texts.append(text)
        self.values.append(value)
        self.vectors = self.vectorizer.fit_transform(self.texts)

    def query(self, text, threshold=0.4):
        if not self.texts:
            return None

        query_vec = self.vectorizer.transform([text])
        sims = cosine_similarity(query_vec, self.vectors)[0]

        best_idx = sims.argmax()
        if sims[best_idx] < threshold:
            return None

        return self.values[best_idx]
