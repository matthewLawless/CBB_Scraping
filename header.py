import dataclasses
from enum import Enum

class Bookmakers(Enum):
    BET365 = 1
    FANDUEL = 2
    BETMG = 3,
    CAESARSSPORTSBOOK = 4
    DRAFTKINGS = 5
    RIVERSCASINO = 6
    UNIBET = 7

class Moneyline:
    
    home = ""
    away = ""
    home_Odds = None
    away_Odds = None
    date = None


    def __init__(self, home, away, date):
        self.home = home
        self.away = away
        self.date = date

    def toString(self):
        return self.date + "\n" + "{:<25}".format(self.home) + " | " + "{:<6}".format(self.home_Odds) + "\n" + "{:<25}".format(self.away)+ " | " + "{:<6}".format(self.away_Odds)
    
    
