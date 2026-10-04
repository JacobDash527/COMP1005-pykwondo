import random
import numpy as np
import matplotlib.pyplot as plt

NAMES = ["Liam Carter", "Maya Patel", "Noah Kim", "Ava Rossi", 
         "Ethan Walsh", "Zoe Nguyen", "Lucas Silva", "Chloe Murphy", 
         "Oliver Tan", "Isla Brooks","Mason Ortiz", "Priya Shah", 
         "Jack Dunn", "Sofia Marino", "Leo Hansen","Ruby Chen", 
         "Henry Adams", "Aisha Khan", "Owen Reid", "Mia Ivanova",
         "Daniel Okafor", "Ella Fraser", "Sam Costa", "Hana Sato", 
         "Max Berg","Grace Lee", "Tom Novak", "Layla Haddad", 
         "Finn O'Brien", "Nina Petrov","Caleb Moore", "Yuki Tanaka", 
         "Ben Foster", "Amara Diallo", "Jake Wilson", "Elena Cruz", 
         "Ravi Menon", "Tess Walker", "Omar Said", "Lily Evans",]
RANK_NAMES = ['white', 'yellow', 'green', 'blue', 'black']
CLUB_NAMES = ['Miyagi Do', 'Cobra Kai', 'Fighting Dragon', 'Eagle Fang']
QUALIFYING = ['strike_challenge', 'kata', 'board_breaking', 'sparring']

""" Order of methods:
        Accessor
        Modifier
        Public (doing methods)
        Private (internal methods __"class_name")"""

class Comp:
    def __init__(self, clubs=None):
        self.timestep = 0
        self.finals = False
        self.clubs = clubs or [Club(CLUB_NAMES[0]), Club(CLUB_NAMES[1]),
                               Club(CLUB_NAMES[2]), Club(CLUB_NAMES[3])]
        self.events = []

    def get_timestep(self):
        return self.timestep

    def get_clubs(self):
        return self.clubs

    def get_events(self):
        return self.events

    def create_schedule(self):
        competitor_list = self.combine_competitors()
        # Initialise each event
        self.events.append(StrikeChallenge(competitor_list))
        self.events.append(Kata(competitor_list))
        self.events.append(BoardBreaking(competitor_list))
    
    # Combine all competitor lists
    def combine_competitors(self):
        return [competitor for club in self.clubs for 
                competitor in club.get_competitors()]

class Competitor:
    def __init__(self, name=None, rank=None, pos=(1,1), club_name=None):
        self.name = name or random.choice(NAMES)
        self.rank = rank or random.choice(RANK_NAMES)
        self.pos = pos
        self.score = random.randint(1, 10)
        self.club_name = club_name

        # Completed events
        self.strike_challenge_complete = False
        self.kata_complete = False
        self.sparring = False
    
    # Return competitor rank
    def get_name(self):
        return self.name

    def get_rank(self):
        return self.rank

    def get_pos(self):
        return self.pos

    def get_score(self):
        return self.score

    def get_club_name(self):
        return self.club_name

    def update_pos(self, pos):
        self.pos = pos


class Club:
    def __init__(self, name=None):
        self.name = name or random.choice(CLUB_NAMES)
        self.competitors = [Competitor(club_name=self.name) for i in range(10)]
        self.score = random.randint(1,10)

    def get_name(self):
        return self.name

    def get_competitors(self):
        return self.competitors
    
    def get_score(self):
        return self.score

class Event:
    def __init__(self, event_type, competitors):
        self.event_type = event_type
        self.competitors = competitors

class StrikeChallenge(Event):
    def __init__(self, competitors):
        super().__init__('strike_challenge', competitors)

class Kata(Event):
    def __init__(self, competitors):
        super().__init__('kata', competitors)

class BoardBreaking(Event):
    def __init__(self, competitors):
        super().__init__('board_breaking', competitors)

class Sparring(Event):
    def __init__(self, competitors):
        super().__init__('sparring', competitors)
