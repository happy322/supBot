import json


class Task:
    def __init__(self, task_value):
        self.keywords = task_value['keywords']
        self.category = task_value['category']
        self.color = task_value['color']
        self.size = task_value['size']

