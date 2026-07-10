class AnalysisHistory:
    def __init__(self, max_items=100):
        self.max_items = max_items
        self.items = []

    def add(self, analysis):
        self.items.append(analysis)
        if len(self.items) > self.max_items:
            self.items.pop(0)

    def latest(self):
        return self.items[-1] if self.items else None

