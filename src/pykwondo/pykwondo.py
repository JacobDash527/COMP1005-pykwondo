import random
import numpy as np
import matplotlib.pyplot as plt

RANK_NAMES = ['white', 'yellow', 'green', 'blue', 'black']
CLUB_NAMES = ['Miyagi Do', 'Cobra Kai']

class Competitor:
    def __init__(self, rank=None, pos=(1,1)):
        self.rank = rank or random.choice(RANK_NAMES)
        self.pos = pos


    def draw(self, ax):
        ax.scatter(self.pos[0], self.pos[1], color=self.rank)

class Comp:
    def __init__(self, clubs=None):
        self.timestep = 0
        self.finals = False
        self.clubs = clubs or [Club(), Club(), Club(), Club()]
        self.arenas = [[Arena(), Arena()], [Arena(), Arena()]]

    def get_timestep(self):
        return self.timestep

    def get_clubs(self):
        return self.clubs

    def get_arenas(self):
        return self.arenas

class Arena:
    def __init__(self):
        self.event = StrikeChallenge()
    
    def get_event(self):
        return self.event.get_name()

class Club:
    def __init__(self, name=None):
        self.name = name or random.choice(CLUB_NAMES)
        self.competitors = [Competitor()]

    def get_name(self):
        return self.name

    def get_competitors(self):
        return self.competitors

class Event:
    def __init__(self, name):
        self.name = name 

    def get_name(self):
        return self.name

class StrikeChallenge(Event):
    def __init__(self):
        super().__init__("Strike Challenge")

class Kata(Event):
    pass

class BoardBreaking(Event):
    pass

class Sparring(Event):
    pass
