import random
import numpy as np
import params
import csv
from pathlib import Path
from statistics import mean, StatisticsError

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

RANK_NAMES = ['white', 'yellow', 'orange', 'green', 'blue', 'purple', 'brown', 'black']
RANK_SKILL = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

CLUB_NAMES = ['Miyagi Do', 'Cobra Kai', 'Fighting Dragon', 'Eagle Fang']
EVENT_NAMES = ['kata', 'kata', 'board_breaking', 'sparring']
SAVES_DIR = Path(__file__).resolve().parent / "saves"

# Import seed from params file, if None exists generate one
seed = params.random_seed
if params.random_seed == None:
    seed = random.randrange(2**32)
print(f"Seed: {seed}")

""" Order of methods:
        Accessor
        Modifier
        Public (doing methods)
        Private (internal methods __"class_name")
"""

class Comp:
    """Class used to represent the competition.

    Contains methods to handle competition simulation.
    
    Parameters
    ----------
    save_name : string
        Passes the save file name.

    Attributes
    ----------
    save_name : string
        Save file name.
    timestep : int
        Current simulation timestep.
    clubs : list
        List of Club objects, generated from last_save.
    events : list
        List of event objects, generated on creation.
    last_save : list
        Last save in the selected save file for each competitor
        [[name (str), club_name (string), rank (string), score (int)]].
    
    Methods
    -------
    get_timestep()
        Returns current simulation timestep as an integer.
    get_clubs()
        Returns list of clubs.
    get_events()
        Returns list of events.
    get_event()
        Returns event object.
    step()
        Calls simulation modifier methods and increments timestep.
    create_schedule()
        Returns a generated event schedule list.
    combine_competitors()
        Returns a list of all competitors in all clubs.
    save()
        Calls __get_save_list() and appends the simulation results as a string 
        to the end of the save csv.
    __get_save_list()
        Returns a nested list containing each competitor, and their attributes 
        [[name (str), club_name (str), rank (str), score (int)]].
    __load(save_name)
        Open the save csv in the selected save file (string) and reads the last
        appended line. Returns the line as a usable list.
    """
    def __init__(self, save_name=None):
        self.save_name = save_name

        self.timestep = 0
        self.clubs = []
        self.events = []
        self.event = None
        self.last_save = None

    
        try:
            self.last_save = self.__load(self.save_name)
        except:
            FileNotFoundError


        for competitor in self.last_save:
            competitor[3] = int(competitor[3])
        
        for name in CLUB_NAMES:
            competitors = []
            for competitor in self.last_save:
                if competitor[1] == name:
                    competitors.append(Competitor(name=competitor[0], 
                                                  club_name=competitor[1], 
                                                  rank=competitor[2]))
            self.clubs.append(Club(name=name, competitors=competitors))

    def get_timestep(self):
        """Returns current simulation timestep"""
        return self.timestep

    def get_clubs(self):
        """Returns list of clubs"""
        return self.clubs
    
    def get_events(self):
        """Returns list of events"""
        return self.events

    def get_event(self):
        """Returns event object"""
        return self.event

    def step(self):
        """Calls simulation modifier methods and increments timestep."""
        self.event = next((e for e in self.events if not e.complete), None)
        
        if self.event is not None:
            if self.event.started is not True: 
                if self.event.get_timestep() > 2:
                    self.event.begin()
                else:
                    print(f"{self.event.get_event_type().capitalize()} will "
                          f"begin in {3-self.event.get_timestep()}")
            if self.event.complete:
                self.event = None
            self.event.step()

        for club in self.clubs:
            club.update_score()
            club.update_accuracy()
        
        self.timestep += 1

    def create_schedule(self):
        """Returns a generated event schedule list."""
        competitor_list = self.combine_competitors()
        # Initialise each event
        self.events.append(StrikeChallenge(competitor_list))
        self.events.append(Kata(competitor_list))
        #self.events.append(BoardBreaking(competitor_list))
    
    # Combine all competitor lists

    def combine_competitors(self):
        """Returns a list of all competitors in all clubs."""
        return [competitor for club in self.clubs for 
                competitor in club.get_competitors()]
    
    # Append simulation results to file
    def save(self):
        """Calls __get_save_list() and appends the simulation results as a
            string to the end of the save csv."""
        with open(f'{SAVES_DIR}/{self.save_name}/save.csv', 'a') as save_file:
            #print(', '.join(str(i) for i in self.__get_save_list()))
            #save_file.write(', '.join(str(i) for i in self.__get_save_list()) + '\n')
            save_file.close()

    # Gets list of competitor data to save to a file
    def __get_save_list(self):
        """Returns a nested list containing each competitor, and their 
           attributes [name (str), club_name (str), rank (str), score (int)]"""
        return [
                [competitor.get_name(),
                 club.get_name(),
                 competitor.get_rank(),
                 competitor.get_score()]
            for club in self.clubs
            for competitor in club.get_competitors()
            ]

    # Load file
    def __load(self, save_name):
        """Open the save csv in the selected save file (string) and reads the 
           last appended line. Returns the line as a usable list.
        
        Parameters
        ----------
        save_name : string
            Passes the save file name.

        Returns
        ----------
        data_list : list
            Nested list containing each competitor, and their attributes 
            [[name (str), club_name (str), rank (str), score (int)]].
        """
        with open(f'{SAVES_DIR}/{save_name}/save.csv', 'r') as save_file:
            data = save_file.readlines()[-1].strip()
            save_file.close()
            data_list = [[i.strip().strip("'\"") 
                               for i in competitor.strip(" []").split(',')] 
                               for competitor in data.split("],")]
            return data_list

class Competitor:
    def __init__(self, name=None, rank=None, pos=(1,1), club_name=None):
        self.name = name or random.choice(NAMES)
        NAMES.remove(self.name)
        self.rank = rank or random.choice(RANK_NAMES)
        self.pos = pos
        self.score = 0
        self.prev_score = 0
        self.accuracy = []
        self.club_name = club_name
        self.in_event = False
        self.strike = ''

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

    def get_prev_score(self):
        return self.prev_score

    def get_club_name(self):
        return self.club_name

    def update_pos(self, pos):
        self.pos = pos

    def update_score(self, score):
        self.prev_score = self.score
        self.score += score

        if self.score // 20 > self.prev_score // 20:
            self.rank_up()

    def move(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def rank_up(self):
        if self.rank != 'black':
            self.rank = RANK_NAMES[RANK_NAMES.index(self.rank)+1]
            print(f"{self.name} ranked up to {self.rank}")


class Club:
    def __init__(self, name=None, competitors=None):
        self.name = name or random.choice(CLUB_NAMES)
        self.competitors = competitors or [Competitor(club_name=self.name) for i in range(10)]
        self.score = 0
        self.accuracy = []

    def get_name(self):
        return self.name

    def get_competitors(self):
        return self.competitors
    
    def get_score(self):
        return self.score

    def get_accuracy(self):
        return self.accuracy

    def update_score(self):
        self.score = sum(competitor.score for competitor in self.competitors)

    def update_accuracy(self):
        try:
            self.accuracy.append(mean(i
                                 for competitor in self.competitors 
                                 for i in competitor.accuracy))
        except:
            StatisticsError

class Event:
    def __init__(self, event_type, competitors):
        self.event_type = event_type
        self.competitors = competitors
        self.complete = False
        self.started = False
        self.timestep = 0

        self.STRIKES = ['punch', 'kick', 'chop', 'block']
        self.MOVE_TUPLES = {
                'f':    (0, -0.5),
                'b':    (0, 0.5),
                'l':    (-0.5, 0),
                'r':    (0.5, 0),
                }
    
    def get_event_type(self):
        return self.event_type

    def get_timestep(self):
        return self.timestep

class StrikeChallenge(Event):
    def __init__(self, competitors):
        super().__init__('strike_challenge', competitors)
        self.moves = ['kick', 'punch', 'chop' 'punch', 'kick', 'kick', 
                      'chop', 'punch', 'punch']

    def begin(self):
        self.started = True
        i = 0
        j = 0
        for competitor in self.competitors:
            competitor.in_event = True
            competitor.update_pos((23+i*5, 5+j*6))
            i += 1
            if i > 6:
                i=0
                j += 1

    def step(self):
        if self.timestep > 5:
            self.complete = True
            for competitor in self.competitors: competitor.in_event = False
        self.timestep += 1

class Kata(Event):
    def __init__(self, competitors):
        super().__init__('kata', competitors)
        self.moves = ['f', 'b', 'l', 'kick', 'f', 'punch', 'l', 'r', 'block',
                      'r', 'b', 'kick', 'f', 'b', 'l', 'chop']

    def begin(self):
        self.started = True
        i = 0
        j = 0
        for competitor in self.competitors:
            competitor.in_event = True
            competitor.update_pos((27+i*3, 10+j*4))
            i += 1
            if i > 9:
                i=0
                j += 1


    def step(self):
        if self.started == True:
            if self.moves == []:
                self.complete = True
                for competitor in self.competitors: competitor.in_event = False
            else:
                for competitor in self.competitors:
                    competitor.strike = ''
                    error = random.uniform(0.0, 1.0)
                    if self.moves[0] in self.MOVE_TUPLES:
                        if error < RANK_SKILL[RANK_NAMES.index(competitor.rank)]:
                            move_xy = self.MOVE_TUPLES[self.moves[0]]
                            competitor.move(move_xy[0], move_xy[1])
                            competitor.update_score(1)
                            competitor.accuracy.append(1)
                        else:
                            competitor.accuracy.append(0)
                    else:
                        competitor.strike = (self.moves[0] 
                                         if error < RANK_SKILL
                                         [RANK_NAMES.index(competitor.rank)] 
                                         else random.choice(self.STRIKES))
                        if competitor.strike == self.moves[0]:
                            competitor.update_score(2)
                            competitor.accuracy.append(1)
                        else:
                            competitor.accuracy.append(0)
                self.moves.pop(0)
        self.timestep += 1
    

class BoardBreaking(Event):
    def __init__(self, competitors):
        super().__init__('board_breaking', competitors)

class Sparring(Event):
    def __init__(self, competitors):
        super().__init__('sparring', competitors)
