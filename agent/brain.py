class Brain:
    def __init__(self):
        # Utility weights (can be learned later)
        self.weights = {
            "accuracy": 1.0,
            "risk": -1.0,
            "cost": -0.3,
            "learning": 0.5
        }

    def build_world_state(self, *, text, intent, confidence,
                          has_symbolic, has_semantic,
                          pending_knowledge):
        return {
            "text": text,
            "intent": intent,
            "confidence": confidence,
            "has_symbolic": has_symbolic,
            "has_semantic": has_semantic,
            "pending_knowledge": pending_knowledge
        }

    def possible_actions(self, state):
        actions = []

        if state["pending_knowledge"]:
            actions.append("CONFIRM_STORAGE")
            actions.append("REJECT_STORAGE")
            return actions

        if state["intent"] == "store_fact":
            actions.append("STORE_FACT")

        if state["intent"] == "recall_fact":
            if state["has_symbolic"]:
                actions.append("ANSWER_FROM_MEMORY")
            elif state["has_semantic"]:
                actions.append("ANSWER_FROM_SEMANTIC")
            else:
                actions.append("USE_WIKIPEDIA")

        if state["confidence"] < 0.45:
            actions.append("USE_WIKIPEDIA")
            actions.append("ASK_CLARIFICATION")

        if not actions:
            actions.append("DO_NOTHING")

        return list(set(actions))

    def utility(self, action, state):
        # Estimated values (heuristic for now)
        accuracy = 0.0
        risk = 0.0
        cost = 0.0
        learning = 0.0

        if action == "ANSWER_FROM_MEMORY":
            accuracy = 0.9
            risk = 0.1

        elif action == "ANSWER_FROM_SEMANTIC":
            accuracy = 0.7
            risk = 0.3

        elif action == "USE_WIKIPEDIA":
            accuracy = 0.9
            risk = 0.1
            cost = 0.4
            learning = 0.3

        elif action == "ASK_CLARIFICATION":
            accuracy = 0.4
            risk = 0.1
            cost = 0.2

        elif action == "STORE_FACT":
            accuracy = 0.8
            risk = 0.2
            learning = 0.6

        elif action == "CONFIRM_STORAGE":
            learning = 1.0

        elif action == "REJECT_STORAGE":
            risk = 0.0

        score = (
            self.weights["accuracy"] * accuracy +
            self.weights["risk"] * risk +
            self.weights["cost"] * cost +
            self.weights["learning"] * learning
        )

        return score

    def decide(self, state):
        actions = self.possible_actions(state)
        scored = {a: self.utility(a, state) for a in actions}
        return max(scored, key=scored.get)
