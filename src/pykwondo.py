import random
import numpy as np
import params
import csv
from pathlib import Path

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

RANK_NAMES = ['white', 'yellow', 'orange', 'green', 'blue', 'purple', 'brown' 'black']
CLUB_NAMES = ['Miyagi Do', 'Cobra Kai', 'Fighting Dragon', 'Eagle Fang']
QUALIFYING = ['strike_challenge', 'kata', 'board_breaking', 'sparring']

# Import seed from params file, if None exists generate one
seed = params.random_seed
if params.random_seed == None:
    seed = random.randrange(2**32)
print(f"Seed: {seed}")

""" Order of methods:
        Accessor
        Modifier
        Public (doing methods)
        Private (internal methods __"class_name")"""


class Comp:
    def __init__(self, save_dir=None):
        self.timestep = 0
        self.finals = False
        self.clubs = []
        self.events = []
        self.save_dir = save_dir
        self.last_save = None
    
        try:
            self.last_save = self.__load()
        except:
            FileNotFoundError

        self.save_list = [[x.strip().strip("'\"") for x in competitor.strip(" []").split(',')]for competitor in self.last_save.split("],")]
        for competitor in self.save_list:
            competitor[3] = int(competitor[3])
        
        for name in CLUB_NAMES:
            competitors = []
            for competitor in self.save_list:
                if competitor[1] == name:
                    competitors.append(Competitor(name=competitor[0], 
                                                  club_name=competitor[1], 
                                                  rank=competitor[2]))
            self.clubs.append(Club(name=name, competitors=competitors))


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
    
    # Append simulation results to file
    def save(self):
        with open(f'saves/{self.save_dir}/save.csv', 'a') as save_file:
            #print(', '.join(str(i) for i in self.__get_save_list()))
            #save_file.write(', '.join(str(i) for i in self.__get_save_list()) + '\n')
            save_file.close()

    # Gets list of competitor data to save to a file
    def __get_save_list(self):
        return [
                [competitor.get_name(),
                 club.get_name(),
                 competitor.get_rank(),
                 competitor.get_score()]
            for club in self.clubs
            for competitor in club.get_competitors()
            ]

    # Load file
    def __load(self):
        with open(f'saves/{self.save_dir}/save.csv', 'r') as save_file:
            data = save_file.readlines()[-1].strip()
            save_file.close()
            return data

class Competitor:
    def __init__(self, name=None, rank=None, pos=(1,1), club_name=None):
        self.name = name or random.choice(NAMES)
        NAMES.remove(self.name)
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
    def __init__(self, name=None, competitors=None):
        self.name = name or random.choice(CLUB_NAMES)
        self.competitors = competitors or [Competitor(club_name=self.name) for i in range(10)]
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
