import parser


class Bot:
    def __init__(self, task, proxy, profile):
        self.parser = parser.Parser(task, proxy)
        self.check_outer = None

    def go(self):
        pass
