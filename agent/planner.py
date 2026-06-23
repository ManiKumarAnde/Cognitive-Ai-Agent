from agent.intent_model import IntentModel

class Planner:
    def __init__(self):
        self.intent_model = IntentModel()
        self.threshold = 0.3

    def decide(self, user_input):
        return self.intent_model.predict(user_input, self.threshold)
