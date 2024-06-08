import dataclasses

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
    
    
