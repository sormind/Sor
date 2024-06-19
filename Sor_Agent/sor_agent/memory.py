# sor_agent/memory.py
import json
import os

class Memory:
    def __init__(self, filename="sor_agent/memory_storage/memory.json"):
        self.filename = filename
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_memory(self):
        with open(self.filename, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def store(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def retrieve(self, key):
        return self.memory.get(key, None)
