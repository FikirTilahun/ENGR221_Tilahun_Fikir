"""
Author: Prof. Alyssa
Defines information for a professor.
You do NOT need to modify this file.
"""

from enum import Enum
import os

from preferences import Preferences

class Professor:
    def __init__(self, first_name, last_name, 
                 program, rank, office):
        self.first_name = first_name
        self.last_name = last_name
        self.program = self.Program.init_from_str(program)
        self.rank = self.Rank.init_from_str(rank)
        self.office = office 

        # Image to display for the faculty
        self.headshot = os.path.join(Preferences.IMG_DIR, f"{last_name.lower()}.gif")

    def __str__(self):
        """ Defines what should be displayed when the object is printed """
        return (f"Name: {self.first_name} {self.last_name}\n" + \
                f"Title: {self.rank.value} Professor of {self.program.value} Engineering\n" + \
                f"Office: {self.office}")
    

    class Rank(Enum):
        ASSISTANT = "Assistant"
        ASSOCIATE = "Associate"
        FULL = "Full"
        
        @classmethod
        def init_from_str(cls, rank):
            return cls[rank.strip().upper()]
        
    class Program(Enum):
        ELECTRICAL = "Electrical"
        COMPUTER = "Computer"
        CIVIL = "Civil"
        MECHANICAL = "Mechanical"

        @classmethod 
        def init_from_str(cls, program):
            print(program)
            return cls[program.strip().upper()]