import dataclasses
from enum import Enum

class Bookmakers(Enum):
    BET365 = 0
    FANDUEL = 1
    BETMGM = 2
    CAESARSSPORTSBOOK = 3
    DRAFTKINGS = 4
    RIVERSCASINO = 5
    UNIBET = 6


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
    

class Total:
    home = ""
    away = ""
    total = None
    under_Odds  = None
    over_Odds = None
    date = None
    bookmaker = ""

    def __init__(self, home, away, date, bookmaker):
        self.home = home
        self.away = away
        self.date = date
        self.bookmaker = bookmaker
    
    def toString(self):
        return self.bookmaker + "  |  " + str(self.date) + "\n" + "{:<25}".format(self.home) + " | O" + "{:<4}".format(self.total) + \
        " | " + "{:<6}".format(self.over_Odds) + "\n" + "{:<25}".format(self.away)+ " | U" + "{:<4}".format(self.total) + " | " + "{:<6}".format(self.under_Odds)