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





def findDate(webpage):
    date = webpage.find_element(By.XPATH, "//*[@id='odds-component']/header")
    data_content = date.get_attribute("data-content")
    # print(data_content)
    dateIndex = data_content.find("date")
    # print(dateIndex)
    # print("[[[[[[[[]]]]]]]]")
    # print(data_content[dateIndex+5:dateIndex + 15])
    return data_content[dateIndex+5:dateIndex + 15]


bookmakerMap = {
    "BET365": 1,
    "FANDUEL": 2,
    "BETMGM": 3,
    "CAESARSSPORTSBOOK": 4,
    "DRAFTKINGS": 5,
    "RIVERSCASINO": 6,
    "UNIBET": 7
}

def createMoneylineFromTwoRows(homeRow, awayRow, webpage, date, bookmakerNumber):
    #need to find out what day it is
    homeTeamName = (homeRow.find_element(By.CLASS_NAME, "team-name")).text
    awayTeamName = (awayRow.find_element(By.CLASS_NAME, "team-name")).text

    m = header.Moneyline(homeTeamName, awayTeamName, date, Bookmakers(bookmakerNumber).name)
    m.home_Odds = ((homeRow.find_elements(By.CLASS_NAME, "game-odds"))[bookmakerNumber]).text
    m.away_Odds = ((awayRow.find_elements(By.CLASS_NAME, "game-odds"))[bookmakerNumber]).text
    return m

#Parses moneyline data from single date. webpage is the page corresponding to the date with moneyline already selected
#this method returns a list of all of the moneyline objects, which will then (in some to-be-created logic)
#be passed to a method that inserts these moneyline objects into the database
def parseMoneylineFromPage(webpage, bookmakerNumber):
    currentRowIndex=0
    result = []
    topRows = webpage.find_elements(By.CLASS_NAME, "divided")
    bottomRows = webpage.find_elements(By.CLASS_NAME, "footer")

    if (len(topRows) != len(bottomRows)):
        raise Exception("Differing number of top and bottom rows")
    
    while (currentRowIndex < len(topRows)):
    # topRowOfPair = sPage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[2]")
    # bottomRowOfPair = sPage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[3]")
        topRowOfPair = topRows[currentRowIndex]
        bottomRowOfPair = bottomRows[currentRowIndex]
        # print((topRowOfPair.find_element(By.CLASS_NAME, "team-name")).text)
        # print((bottomRowOfPair.find_element(By.CLASS_NAME, "team-name")).text)
        m = createMoneylineFromTwoRows(topRowOfPair, bottomRowOfPair, sPage, date, bookmakerNumber)
        result.append(m)
        currentRowIndex+=1
    
    return result

# def insertMoneylineObjectsIntoDatabase(moneylineList):


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

moneylineList = parseMoneylineFromPage(moneyline, Bookmakers["FANDUEL"].value)

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



