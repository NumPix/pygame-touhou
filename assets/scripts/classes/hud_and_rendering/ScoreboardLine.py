from datetime import datetime


class ScoreboardLine:
    def __init__(self, name, score, date, slow, player=False):
        self.name = name
        self.score = score
        self.date = date
        self.slow = slow
        self.player = player

    def mask(self):
        return [self.score, datetime.now() - datetime.strptime(self.date, "%d/%m/%y"), -self.slow]

    def get_values(self):
        return self.name, self.score, self.date, self.slow

    def __gt__(self, other):
        return self.mask() > other.mask()

    def __eq__(self, other):
        return self.mask() == other.mask()

    def __str__(self):
        return '     '.join(map(str, [self.name, '{:8}'.format(self.score), self.date if self.date != "01/01/70" else "--/--/--", self.slow]))