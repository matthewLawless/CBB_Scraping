import dataclasses
from enum import Enum

class Bookmakers(Enum):
    BET365 = 1
    FANDUEL = 2
    BETMGM = 3
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
    bookmaker = ""


    def __init__(self, home, away, date, bookmaker):
        self.home = home
        self.away = away
        self.date = date
        self.bookmaker = bookmaker

    def toString(self):
        return self.bookmaker + "  |  " + str(self.date) + "\n" + "{:<25}".format(self.home) + " | " + "{:<6}".format(self.home_Odds) + "\n" + "{:<25}".format(self.away)+ " | " + "{:<6}".format(self.away_Odds)
    
    
class Spread:
    home = ""
    away = ""
    home_Spread = None
    away_Spread = None
    home_Odds = None
    away_Odds = None
    date = None
    bookmaker = ""

    def __init__(self, home, away, date, bookmaker):
        self.home = home
        self.away = away
        self.date = date
        self.bookmaker = bookmaker

    def toString(self):
        return self.bookmaker + "  |  " + str(self.date) + "\n" + "{:<25}".format(self.home) + " | " + "{:<4}".format(self.home_Spread) + \
        " | " + "{:<6}".format(self.home_Odds) + "\n" + "{:<25}".format(self.away)+ " | " + "{:<4}".format(self.away_Spread) + " | " + "{:<6}".format(self.away_Odds)