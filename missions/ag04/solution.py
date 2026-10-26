import re


class Memory:
    def __init__(self, budget):
        self.budget = budget
        self.messages = []

    def add(self, role, text, pinned=False):
        self.messages.append((role, text))

    def context(self):
        return list(self.messages)


m = Memory(budget=12)
m.add("user", "I am allergic to penicillin", pinned=True)
m.add("user", "My number is 555 010 0199 and my email is sam@example.com")
print(m.context())
