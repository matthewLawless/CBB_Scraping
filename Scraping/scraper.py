import bs4
import requests
from requests_html import HTMLSession
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import header
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import StaleElementReferenceException
from selenium.common import ElementClickInterceptedException
from header import Bookmakers
import mysql.connector
import datetime
from datetime import date
from sql_creds import Credentials
import calendar
from selenium.common import ElementNotInteractableException

cbb_betting_lines = mysql.connector.connect(
    host =  (Credentials.host).value,
    user =  (Credentials.user).value,
    password = (Credentials.password).value,
    database = (Credentials.database.value),
    )



def findDate(webpage):
    date = webpage.find_element(By.XPATH, "//*[@id='odds-component']/header")
    data_content = date.get_attribute("data-content")
    # print(data_content)
    dateIndex = data_content.find("date")
    # print(dateIndex)
    # print("[[[[[[[[]]]]]]]]")
    # print(data_content[dateIndex+5:dateIndex + 15])
    return (data_content[dateIndex+5:dateIndex + 15])

def dateStringToDateObject(dateString):
    # print(int(dateString[0:4]))
    # print(int(dateString[5:7]))
    # print(int(dateString[8:10]))
    return datetime.date(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:10]))


bookmakerMap = {
    "BET365": 1,
    "FANDUEL": 2,
    "BETMGM": 3,
    "CAESARSSPORTSBOOK": 4,
    "DRAFTKINGS": 5,
    "RIVERSCASINO": 6,
    "UNIBET": 7
}

def createSpreadFromTwoRows(homeRow, awayRow, webpage, date, bookmakerNumber):
    homeTeamName = (homeRow.find_element(By.CLASS_NAME, "team-name")).text
    awayTeamName = (awayRow.find_element(By.CLASS_NAME, "team-name")).text
    print(homeTeamName)
    print(awayTeamName)
    

    s = header.Spread(homeTeamName, awayTeamName, date, Bookmakers(bookmakerNumber).name)


    homeGameOdds = homeRow.find_elements(By.CLASS_NAME, "game-odds")
    homeString = homeGameOdds[bookmakerNumber].text

    if (homeString == 'N/A'):
        return None

    homeStringArray = homeString.split('\n')
    s.home_Spread = homeStringArray[0]
    s.home_Odds = homeStringArray[1]

    awayGameOdds = awayRow.find_elements(By.CLASS_NAME, "game-odds")
    awayString = awayGameOdds[bookmakerNumber].text
    awayStringArray = awayString.split('\n')
    s.away_Spread = awayStringArray[0]
    s.away_Odds = awayStringArray[1]


    # s.home_Spread = ((homeRow.find_elements(By.CLASS_NAME, "data-value"))[bookmakerNumber]).text
    # if (s.home_Spread == "N/A"):
    #     s.home_Odds = "N/A"
    # else: 
    #     s.home_Odds = ((homeRow.find_elements(By.CLASS_NAME, "data-odds"))[bookmakerNumber]).text

    # s.away_Spread = ((awayRow.find_elements(By.CLASS_NAME, "data-value"))[bookmakerNumber]).text
    # if (s.away_Spread == "N/A"):
    #     s.away_Odds = "N/A"
    # else: 
    #     s.away_Odds = ((awayRow.find_elements(By.CLASS_NAME, "data-odds"))[bookmakerNumber]).text

    if (homeTeamName == '' and awayTeamName == ''):
        return None
    
    return s


def createMoneylineFromTwoRows(homeRow, awayRow, webpage, date, bookmakerNumber):
    
    homeTeamName = (homeRow.find_element(By.CLASS_NAME, "team-name")).text
    awayTeamName = (awayRow.find_element(By.CLASS_NAME, "team-name")).text

    m = header.Moneyline(homeTeamName, awayTeamName, date, Bookmakers(bookmakerNumber).name)

    gameOdds = (homeRow.find_elements(By.CLASS_NAME, "game-odds"))
    m.home_Odds = (gameOdds[bookmakerNumber]).text

    if (m.home_Odds == 'N/A'):
        return None
    
    m.away_Odds = ((awayRow.find_elements(By.CLASS_NAME, "game-odds"))[bookmakerNumber]).text
    
    if (homeTeamName == '' and awayTeamName == ''):
        return None
    
    return m

def createTotalFromTwoRows(homeRow, awayRow, webpage, date, bookmakerNumber):
    homeTeamName = (homeRow.find_element(By.CLASS_NAME, "team-name")).text
    awayTeamName = (awayRow.find_element(By.CLASS_NAME, "team-name")).text

    t = header.Total(homeTeamName, awayTeamName, date, Bookmakers(bookmakerNumber).name)

    homeGameOdds = (homeRow.find_elements(By.CLASS_NAME, "game-odds"))
    homeString = homeGameOdds[bookmakerNumber].text

    if (homeString == 'N/A'):
        return None

    homeStringArray = homeString.split('\n')
    t.over_Odds = homeStringArray[1]
    
    t.total = (homeStringArray[0])[1:]

    awayGameOdds = (awayRow.find_elements(By.CLASS_NAME, "game-odds"))
    awayString = awayGameOdds[bookmakerNumber].text
    awayStringArray = awayString.split('\n')
    t.under_Odds = awayStringArray[1]

    # if (t.total != '/A'):
    #     t.over_Odds = (((homeRow.find_elements(By.CLASS_NAME, "data-odds"))[bookmakerNumber]).text)
    #     t.under_Odds = (((awayRow.find_elements(By.CLASS_NAME, "data-odds"))[bookmakerNumber]).text)
    # else:
    #     return None

    if (homeTeamName == '' and awayTeamName == ''):
        return None
    
    return t

def parseTotalFromPage(webpage, bookmakerNumber):
    currentRowIndex=0
    result = []
    totalOnlyGames = webpage.find_element(By.XPATH, "//*[@id='odds-table-total--0']")
    topRows = totalOnlyGames.find_elements(By.CLASS_NAME, "divided")
    bottomRows = totalOnlyGames.find_elements(By.CLASS_NAME, "footer")
    websiteDate = (dateStringToDateObject(findDate(webpage)))
    while (currentRowIndex < len(topRows)):
        topRowOfPair = topRows[currentRowIndex]
        bottomRowOfPair = bottomRows[currentRowIndex]
        s = createTotalFromTwoRows(topRowOfPair, bottomRowOfPair, sPage, websiteDate, bookmakerNumber)
        if (s != None):
            result.append(s)
        currentRowIndex+=1

    return result



def parseSpreadFromPage(webpage, bookmakerNumber):
    currentRowIndex=0
    result = []
    spreadOnlyGames = webpage.find_element(By.XPATH, "//*[@id='odds-table-spread--0']")
    topRows = spreadOnlyGames.find_elements(By.CLASS_NAME, "divided")
    bottomRows = spreadOnlyGames.find_elements(By.CLASS_NAME, "footer")
    print("topRows amount: " + str(len(topRows)))
    print("bottomRows amount: " + str(len(bottomRows)))
    print("#######################################################################")

    websiteDate = (dateStringToDateObject(findDate(webpage)))
    
    while (currentRowIndex < len(topRows)):
        topRowOfPair = topRows[currentRowIndex]
        bottomRowOfPair = bottomRows[currentRowIndex]
        s = createSpreadFromTwoRows(topRowOfPair, bottomRowOfPair, sPage, websiteDate, bookmakerNumber)
        if (s != None):
            result.append(s)
        currentRowIndex+=1

    return result


#Parses moneyline data from single date. webpage is the page corresponding to the date with moneyline already selected
#this method returns a list of all of the moneyline objects, which will then (in some to-be-created logic)
#be passed to a method that inserts these moneyline objects into the database
def parseMoneylineFromPage(webpage, bookmakerNumber):
    currentRowIndex=0
    result = []
    moneylineOnlyGames = webpage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']")
    topRows = moneylineOnlyGames.find_elements(By.CLASS_NAME, "divided")
    bottomRows = moneylineOnlyGames.find_elements(By.CLASS_NAME, "footer")

    websiteDate = (dateStringToDateObject(findDate(webpage)))

    if (len(topRows) != len(bottomRows)):
        raise Exception("Differing number of top and bottom rows")
    
    while (currentRowIndex < len(topRows)):
    # topRowOfPair = sPage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[2]")
    # bottomRowOfPair = sPage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[3]")
        topRowOfPair = topRows[currentRowIndex]
        bottomRowOfPair = bottomRows[currentRowIndex]
        # print((topRowOfPair.find_element(By.CLASS_NAME, "team-name")).text)
        # print((bottomRowOfPair.find_element(By.CLASS_NAME, "team-name")).text)
        m = createMoneylineFromTwoRows(topRowOfPair, bottomRowOfPair, sPage, websiteDate, bookmakerNumber)
        if (m != None):
            result.append(m)
        currentRowIndex+=1
    
    return result

def retryClick(webpageElement, retries):
    counter = 0
    while (counter < retries):
        try:
            webpageElement.click()
            return
        except StaleElementReferenceException:
            counter+=1
            time.sleep(0.1)
    
    raise StaleElementReferenceException
        
def insertSpreadObjectsIntoDatabase(spreadList, databaseCursor):
    numberOfRows = len(spreadList)
    insertStatement = "INSERT INTO spread(home, away, date, home_Spread, away_Spread, home_Odds, away_Odds, bookmaker)\nVALUES\n"
    for s in spreadList:
        row = '("%s", "%s", "%s", %.1f, %.1f, %d, %d, "%s")' % (s.home, s.away, s.date, float(s.home_Spread), float(s.away_Spread), int(s.home_Odds), int(s.away_Odds), s.bookmaker)
        insertStatement += row
        insertStatement += ',\n'

    insertStatement = insertStatement[:-2]
    insertStatement += ";"

    print(insertStatement)

    databaseCursor.execute(insertStatement)
    
def insertTotalObjectsIntoDatabase(totalList, databaseCursor):
    insertStatement = "INSERT INTO total(home, away, date, total, over_Odds, under_Odds, bookmaker)\nVALUES\n"
    for t in totalList:
        row = '("%s", "%s", "%s", %.1f, %d, %d, "%s")' % (t.home, t.away, t.date, float(t.total), int(t.over_Odds), int(t.under_Odds), t.bookmaker)
        insertStatement += row
        insertStatement += ',\n'

    insertStatement = insertStatement[:-2]
    insertStatement += ";"
    
    print(insertStatement)

    databaseCursor.execute(insertStatement)

def insertMoneylineObjectsIntoDatabase(moneylineList, databaseCursor):
    numberOfRows = len(moneylineList)
    insertStatement = "INSERT INTO moneyline(home, away, date, home_Odds, away_Odds, bookmaker)\nVALUES \n"
    for m in moneylineList:
        
        if (m.home_Odds == 'N/A' and m.away_Odds == 'N/A'):
            row = '("%s", "%s", "%s", %s, %s, "%s")' % (m.home, m.away, m.date, 'NULL', 'NULL', m.bookmaker)
        else:
            hOdds = m.home_Odds
            aOdds = m.away_Odds
            if (m.home_Odds[0] == '-'):
                hOdds = '-' + m.home_Odds
            
            if (m.away_Odds[0] == '-'):
                aOdds = '-' + m.away_Odds
            
                
            #row = '("%s", "%s", "%s", %d, %d, "%s")' % (m.home, m.away, m.date, int((m.home_Odds)[1:]), int((m.away_Odds)[1:]), m.bookmaker)
            row = '("%s", "%s", "%s", %d, %d, "%s")' % (m.home, m.away, m.date, int((hOdds)[1:]), int((aOdds)[1:]), m.bookmaker)
        insertStatement += row
        insertStatement += ',\n'


    insertStatement = insertStatement[:-2]
    insertStatement += ";"
    print(insertStatement)
    databaseCursor.execute(insertStatement)

#If we are in the same month as the desired date, we use previous and next
#otherwise, we 
def pathToDay(desiredDate, webpage):
    dropDownForCalendar = webpage.find_element(By.CLASS_NAME, "down")
    dropDownForCalendar.click()

    currentMonthAndYear = webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[8]/div/div/span[2]")
    # monthAndYearText = currentMonthAndYear.text
    # print("Month Year: " + monthAndYearText)
    # monthAbbreviation = monthAndYearText[0:-5]
    # websiteYear = int(monthAndYearText[-4:])
    # print("monthAbbreviation ==>: " + monthAbbreviation)
    # print("year ==>: ", websiteYear)
    # print(date.year)
    # print(date.month)
    # websiteDayOfMonthComp = webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[4]")
    # websiteDayOfMonth = int((websiteDayOfMonthComp.text)[-2:])
    # print(websiteDayOfMonth)
    # print(int(websiteDayOfMonth))
    # print("---------------------------")
    # websiteDateText = (webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[4]")).
    websiteDate = (dateStringToDateObject(findDate(webpage)))
    print(findDate(webpage))
    print(dateStringToDateObject(findDate(webpage)))
    print((dateStringToDateObject(findDate(webpage))).__class__)

    lastIterationDate = datetime.date(2000, 3, 3)



    while (True):
        #datetime.date(websiteYear, list(calendar.monthAbbreviation).index(monthAbbreviation), websiteDayOfMonth) != date
        time.sleep(1)
        websiteDate = (dateStringToDateObject(findDate(webpage)))
        count = 0
        while (count < 10):
            if (websiteDate == lastIterationDate):
                time.sleep(2)
                count+=1
            else:
                break
        count = 0
        
        if (websiteDate.month != desiredDate.month):
            try:
                dropDownForCalendar = webpage.find_element(By.CLASS_NAME, "down")
                dropDownForCalendar.click()
                retryClick(dropDownForCalendar, 50)
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException:
                pass

        websiteDate = (dateStringToDateObject(findDate(webpage)))
        print("website Date ==> " + str(websiteDate))
        previousMonthButton = webpage.find_element(By.CLASS_NAME, "prev")
        nextMonthButton = webpage.find_element(By.CLASS_NAME, "next")
        nextDayButton = webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[5]")
        previousDayButton = webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[3]")

        if (websiteDate.year != desiredDate.year):
            if (websiteDate.year > desiredDate.year):
                previousMonthButton.click()
                #(webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[8]/div/table/tbody/tr[1]/td[2]/span")).click()
                calendarDays = (webpage.find_elements(By.CLASS_NAME, "calendar-day"))
                for c in calendarDays:
                    if (c.text == '1'):
                        c.click()
                        break
            elif (websiteDate.year < desiredDate.year):
                nextMonthButton.click()
                #(webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[8]/div/table/tbody/tr[1]/td[2]/span")).click()
                calendarDays = (webpage.find_elements(By.CLASS_NAME, "calendar-day"))
                for c in calendarDays:
                    if (c.text == '1'):
                        c.click()
                        break

        elif (websiteDate.month != desiredDate.month):
            if (websiteDate.month > desiredDate.month):
                previousMonthButton.click()
                calendarDays = (webpage.find_elements(By.CLASS_NAME, "calendar-day"))
                for c in calendarDays:
                    if (c.text == '1'):
                        c.click()
                        break
            elif (websiteDate.month < desiredDate.month):
                nextMonthButton.click()
                calendarDays = (webpage.find_elements(By.CLASS_NAME, "calendar-day"))
                for c in calendarDays:
                    if (c.text == '1'):
                        c.click()
                        break

        elif (websiteDate.day != desiredDate.day):
            
            if (websiteDate.day > desiredDate.day):
                #(webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[4]")).click()
                #previousDayButton.click()
                retryClick(previousDayButton, 50)

            if (websiteDate.day < desiredDate.day):
                #(webpage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[4]")).click()
                #nextDayButton.click()
                retryClick(nextDayButton, 50)
        
        else:
            break

        lastIterationDate = websiteDate
            
def dayHasGames(webpage):
    dividedElements = webpage.find_elements(By.CLASS_NAME, "divided")
    return (len(dividedElements) != 0)
        

        







URL = "https://www.vegasinsider.com/college-basketball/odds/las-vegas/"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
weekDays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
#Dictionary maps Months to Booleans where the boolean is true if the month has 31 days false otherwise
monthHas31Days = {
    "Jan": True,
    "Feb": False,
    "Mar": True,
    "Apr": False,
    "May": True,
    "Jun": False,
    "Jul": True, 
    "Aug": True,
    "Sep": False, 
    "Oct": True, 
    "Nov": False, 
    "Dec": True
}

page = requests.get(URL)

sPage = webdriver.Chrome()
sPage.maximize_window()
sPage.get(URL)



# print("-----------------------")
# print(dayHasGames(sPage))
# print("-----------------------")
# time.sleep(2)
# pathToDay(datetime.date(2023, 8, 25), sPage)
# print("-----------------------")
# print(dayHasGames(sPage))
# print("-----------------------")
# time.sleep(2)
# pathToDay(datetime.date(2023, 11, 9), sPage)
# print("-----------------------")
# print(dayHasGames(sPage))
# print("-----------------------")

pathToDay(datetime.date(2023, 11, 8), sPage)
attempts = 0
while (attempts < 50):
    try:
        (sPage.find_element(By.XPATH, "//*[@id='odds-component']/div/ul/li[2]/span")).click()
        break
    except StaleElementReferenceException:
        attempts+=1

totals = parseTotalFromPage(sPage, Bookmakers["BETMGM"].value)



# sPage.close()


attempts = 0
while (attempts < 50):
    try:
        (sPage.find_element(By.XPATH, "//*[@id='odds-component']/div/ul/li[3]/span")).click()
        break
    except StaleElementReferenceException:
        attempts+=1

moneylines = parseMoneylineFromPage(sPage, Bookmakers["BETMGM"].value)


attempts = 0
while (attempts < 50):
    try:
        (sPage.find_element(By.XPATH, "//*[@id='odds-component']/div/ul/li[1]/span")).click()
        break
    except StaleElementReferenceException:
        attempts+=1  


spreads = parseSpreadFromPage(sPage, Bookmakers["BETMGM"].value)



for s in spreads:
    print(s.toString())

for t in totals:
    print(t.toString())

for m in moneylines:
    print(m.toString())

cursor = cbb_betting_lines.cursor()
insertSpreadObjectsIntoDatabase(spreads, cursor)
insertTotalObjectsIntoDatabase(totals, cursor)

cbb_betting_lines.commit()
sPage.close()






dropDownForCalendar = sPage.find_element(By.CLASS_NAME, "down")
dropDownForCalendar.click()

currentMonth = sPage.find_element(By.CLASS_NAME, "current")
previousCalendarButton = sPage.find_element(By.CLASS_NAME, "prev")

while ("Nov" not in currentMonth.text):
    previousCalendarButton.click()
    print("currentMonth ==> ", currentMonth.text)

days = sPage.find_elements(By.CLASS_NAME, "calendar-day")
#days = sPage.find_element(By.XPATH, )
for d in days:
    print(d.text)
    if (d.text == "1"):
        d.click()
        break

print("------------------done with loop----------------------")
foundDateWithLines = False
while (True):
    time.sleep(0.1)
    try:
        sPage.find_element(By.XPATH, "//*[@id='odds-table-spread--0']/tr[2]")
        print("----------found odds table------------")
        foundDateWithLines = True
        break    
    except NoSuchElementException:
        print ("-------------got past the try statement-----------")
        #No betting data for this day --> go to next day
        activeDate = sPage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[4]")
        print("------------------finding the element went fine--------------------")
        dateInList = (activeDate.text.split('\n'))
        print(dateInList[0])
        print(dateInList[1])
        #nextDay = sPage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[5]")
        #nextDay.click()
        attempts = 0
        success = False
        while (attempts < 50):
            try:
                if (success == True):
                    break
                else:
                    (sPage.find_element(By.XPATH, "//*[@id='odds-component']/header/div/div/div/div/div[5]")).click()
                    success = True
                        
            except StaleElementReferenceException:
                #do nothing
                attempts+=1
            except ElementClickInterceptedException:
                attempts+=1
            
                    


#Switch to moneyline tables
attempts = 0
while (attempts < 50):
    try:
        (sPage.find_element(By.XPATH, "//*[@id='odds-component']/div/ul/li[3]/span")).click()
        break
    except StaleElementReferenceException:
        attempts+=1


time.sleep(1)
date = findDate(sPage)

moneyline = sPage.find_element(By.XPATH, "//*[@id='odds-component']/div")

moneylineList = parseMoneylineFromPage(moneyline, Bookmakers["DRAFTKINGS"].value)

insertMoneylineObjectsIntoDatabase(moneylineList, cbb_betting_lines.cursor())
cbb_betting_lines.commit()

# currentRowIndex = 0
# topRows = moneyline.find_elements(By.CLASS_NAME, "divided")
# bottomRows = moneyline.find_elements(By.CLASS_NAME, "footer")

# print(len(topRows), " | " ,len(bottomRows))

# for element in topRows:
#     print((element.find_element(By.CLASS_NAME, "game-team")).text)


# if (len(topRows) != len(bottomRows)):
#     raise Exception("Differing number of top and bottom rows")

# while (currentRowIndex < len(topRows)):
#     # topRowOfPair = sPage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[2]")
#     # bottomRowOfPair = sPage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[3]")
#     topRowOfPair = topRows[currentRowIndex]
#     bottomRowOfPair = bottomRows[currentRowIndex]
#     print((topRowOfPair.find_element(By.CLASS_NAME, "team-name")).text)
#     print((bottomRowOfPair.find_element(By.CLASS_NAME, "team-name")).text)
#     m = createMoneylineFromTwoRows(topRowOfPair, bottomRowOfPair, sPage, date)
#     print(m.toString())
#     currentRowIndex+=1




sPage.close()
# print(currentRow.text)
# print((currentRow.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[2]/td[1]")).text)
# print((currentRow.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[3]/td[1]")).text)



for m in moneylineList:
    if (m == None):
        print('NONE')
    else:
        print(m.toString())
    print('\n')

    

#print("days.text ==> ", days.text)
#print("days ==> ", days.accessible_name)


#print(fake_Page.text)
# print("====================")
# session = HTMLSession()

# r = session.get(URL)
# r.html.render(sleep=1)



#print(r.status_code)

#class Client(QWebEnginePage):
#    def __init__(self, url):
#        self.app = QGuiApplication(sys.argv)
#        QWebPage.__init__(self)
#        self.loadFinished.connect(self.on_page_load)



