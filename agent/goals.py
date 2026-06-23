class Goal:
    def __init__(self, description):
        self.description = description
        self.completed = False

    def mark_done(self):
        self.completed = True
