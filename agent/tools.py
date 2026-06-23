import wikipedia
import re
from difflib import get_close_matches


# -------------------------------
# SPELL CORRECTOR (FOR WIKI ONLY)
# -------------------------------
class SpellCorrector:
    VOCABULARY = {
        "chief", "minister", "prime", "president", "capital",
        "india", "andhra", "pradesh", "tamil", "nadu",
        "captain", "team", "cricket", "football",
        "neural", "networks", "machine", "learning",
        "mumbai", "chennai", "kolkata", "bangalore"
    }

    def correct(self, text: str) -> str:
        words = text.split()
        corrected = []

        for word in words:
            w = word.lower()
            if w.isdigit() or w in self.VOCABULARY:
                corrected.append(word)
                continue

            match = get_close_matches(w, self.VOCABULARY, n=1, cutoff=0.85)
            corrected.append(match[0] if match else word)

        return " ".join(corrected)


# -------------------------------
# WIKIPEDIA TOOL
# -------------------------------
class WikipediaTool:
    def __init__(self):
        self.cache = {}
        self.spell = SpellCorrector()

    def _clean_query(self, query: str) -> str:
        query = query.lower().strip()
        query = query.replace('"', '').replace("'", "")

        query = re.sub(
            r"\b(who is|what is|tell me|explain|current|present)\b",
            "",
            query
        )

        query = re.sub(r"\s+", " ", query).strip()
        query = self.spell.correct(query)

        return query

    def search(self, query, sentences=2):
        query = self._clean_query(query)

        if query in self.cache:
            return self.cache[query]

        result = None

        try:
            result = wikipedia.summary(query, sentences=sentences)
        except:
            pass

        if not result:
            try:
                results = wikipedia.search(query)
                if results:
                    result = wikipedia.summary(results[0], sentences=sentences)
            except:
                pass

        if result:
            self.cache[query] = result

        return result


# -------------------------------
# CALCULATOR TOOL (FIXED)
# -------------------------------
class CalculatorTool:
    ALLOWED_CHARS = set("0123456789+-*/(). ")

    WORD_TO_SYMBOL = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "times": "*",
        "multiply": "*",
        "into": "*",
        "x": "*",
        "divide": "/",
        "divided": "/",
        "by": "",
    }

    def normalize_math_text(self, text: str) -> str:
        text = text.lower()

        for word, symbol in self.WORD_TO_SYMBOL.items():
            text = re.sub(rf"\b{word}\b", symbol, text)

        text = re.sub(r"[a-z]", "", text)  # remove remaining words
        return text.strip()

    def can_calculate(self, text: str) -> bool:
        expr = self.normalize_math_text(text)
        return (
            any(op in expr for op in "+-*/")
            and all(c in self.ALLOWED_CHARS for c in expr)
        )

    def calculate(self, text: str):
        expr = self.normalize_math_text(text)
        try:
            return eval(expr, {"__builtins__": {}}, {})
        except:
            return None


# -------------------------------
# TOOL MANAGER
# -------------------------------
class ToolManager:
    def __init__(self):
        self.wikipedia = WikipediaTool()
        self.calculator = CalculatorTool()

    def use_wikipedia(self, query):
        return self.wikipedia.search(query)

    def can_calculate(self, text):
        return self.calculator.can_calculate(text)

    def use_calculator(self, text):
        return self.calculator.calculate(text)
