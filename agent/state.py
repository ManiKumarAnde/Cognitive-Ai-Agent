import json
import os

class AgentState:
    def __init__(self, memory_file="memory.json"):
        self.knowledge = {}
        self.history = []
        self.memory_file = memory_file
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.knowledge = json.load(f)

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.knowledge, f, indent=4)

    def update_knowledge(self, key, value):
        self.knowledge[key] = value
        self.save_memory()

    def remember(self, event):
        self.history.append(event)
