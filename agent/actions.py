import random


class Actions:
    def __init__(self):
        self.greetings = [
            "Hello! How can I help you today?",
            "Hi there! What would you like to know?",
            "Hey! I'm ready to help.",
            "Hello! Ask me anything.",
            "Hi! How can I assist you?"
        ]

        self.farewells = [
            "Goodbye! Have a great day.",
            "See you later!",
            "Bye! Take care.",
            "It was nice talking to you."
        ]

    def greet(self):
        return random.choice(self.greetings)

    def farewell(self):
        return random.choice(self.farewells)

    def unknown(self):
        return "I'm not sure how to help with that yet."
