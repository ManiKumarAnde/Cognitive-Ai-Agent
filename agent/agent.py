from agent.state import AgentState
from agent.planner import Planner
from agent.actions import Actions
from agent.tools import ToolManager
from agent.llm_engine import LLMEngine


class Agent:
    def __init__(self):
        self.state = AgentState()
        self.planner = Planner()
        self.actions = Actions()
        self.tools = ToolManager()
        self.llm = LLMEngine()

        self.greeting_words = {
            "hi", "hello", "hey", "hii", "hai",
            "good morning", "good afternoon", "good evening"
        }

        self.farewell_words = {
            "bye", "goodbye", "see you", "exit", "quit"
        }

    def perceive(self, user_input: str):
        self.state.remember(user_input)

    def think_and_act(self, user_input: str) -> str:
        self.perceive(user_input)

        text = user_input.strip()
        text_lower = text.lower()

        # -------------------------------
        # 1️⃣ GREETINGS / FAREWELLS
        # -------------------------------
        if text_lower in self.greeting_words:
            return self.actions.greet()

        if text_lower in self.farewell_words:
            return self.actions.farewell()

        # -------------------------------
        # 2️⃣ CALCULATOR
        # -------------------------------
        if self.tools.can_calculate(text):
            result = self.tools.use_calculator(text)
            if result is not None:
                return f"The result is {result}"

        # -------------------------------
        # 3️⃣ PERSONAL MEMORY (STORE)
        # -------------------------------
        if text_lower.startswith("my ") and " is " in text_lower:
            parts = text_lower.split(" is ", 1)
            key = parts[0].replace("my", "").strip()
            value = parts[1].strip()

            if key and value:
                self.state.update_knowledge(key, value)
                return f"Okay, I will remember your {key}."

        # -------------------------------
        # 4️⃣ PERSONAL MEMORY (RECALL)
        # -------------------------------
        if text_lower.startswith("what is my"):
            key = text_lower.replace("what is my", "").replace("?", "").strip()
            value = self.state.knowledge.get(key)

            if value:
                return f"Your {key} is {value}"
            else:
                return f"I don’t know your {key} yet."

        # -------------------------------
        # 5️⃣ INTENT + CONFIDENCE
        # -------------------------------
        decision, confidence = self.planner.decide(text)
        print(f"[DEBUG] intent: {decision} | confidence: {confidence}")

        # -------------------------------
        # 6️⃣ EXPLANATION (LLM – INFORMATIVE MODE)
        # -------------------------------
        if decision == "explain":
            prompt = (
                "You are a clear and knowledgeable assistant. "
                "Explain the following topic in a simple, structured way:\n\n"
                f"{text}"
            )
            return self.llm.generate(prompt)

        # -------------------------------
        # 7️⃣ WORLD FACTS (WIKIPEDIA)
        # -------------------------------
        if decision == "recall_fact" or confidence < 0.5:
            print("[Brain] action: USE_WIKIPEDIA")

            wiki_content = self.tools.use_wikipedia(text)
            if wiki_content:
                return wiki_content.split(".")[0].strip()

        # -------------------------------
        # 8️⃣ DIRECT ANSWER (LLM – NEUTRAL MODE)
        # -------------------------------
        if decision == "answer":
            prompt = (
                "Answer the following question clearly and concisely:\n\n"
                f"{text}"
            )
            return self.llm.generate(prompt)

        # -------------------------------
        # 9️⃣ FRIENDLY CONVERSATION (LLM – SOCIAL MODE)
        # -------------------------------
        friendly_prompt = (
            "You are a friendly, supportive conversational AI. "
            "Respond naturally like a helpful friend. "
            "Do not give technical explanations unless asked.\n\n"
            f"User: {text}\n"
            "Assistant:"
        )
        return self.llm.generate(friendly_prompt)
