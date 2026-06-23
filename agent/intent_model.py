from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class IntentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self._train()

    def _train(self):
        texts = [
            # -------- store facts --------
            "my name is mani",
            "my age is 22",
            "my college is jntua",
            "i live in kakinada",

            # -------- recall facts --------
            "what is my name",
            "tell me my name",
            "what is my age",
            "how old am i",
            "what is my college",
            "where do i live",
            "tell me where do i live",

            # -------- other intents --------
            "explain artificial intelligence",
            "explain machine learning",
            "what is ai",
            "how does ai work",
            "hello",
            "hi"
        ]

        labels = [
            "store_fact",
            "store_fact",
            "store_fact",
            "store_fact",

            "recall_fact",
            "recall_fact",
            "recall_fact",
            "recall_fact",
            "recall_fact",
            "recall_fact",
            "recall_fact",

            "explain",
            "explain",
            "answer",
            "answer",
            "unknown",
            "unknown"
        ]

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict(self, text, threshold=0.3):
        X = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X)[0]

        best_idx = probs.argmax()
        best_prob = probs[best_idx]
        best_intent = self.model.classes_[best_idx]

        if best_prob < threshold:
            return "unknown", best_prob

        return best_intent, best_prob
