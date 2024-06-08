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



m = header.Moneyline("dog", "cat", "d")


fake_URL = "https://realpython.github.io/fake-jobs/"
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


fake_Page = requests.get(fake_URL)
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
    time.sleep(0.5)
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
currentRow = sPage.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[2]")
print(currentRow.text)
print((currentRow.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[2]/td[1]")).text)
print((currentRow.find_element(By.XPATH, "//*[@id='odds-table-moneyline--0']/tr[3]/td[1]")).text)



    

#print("days.text ==> ", days.text)
#print("days ==> ", days.accessible_name)


#print(fake_Page.text)
print("====================")
session = HTMLSession()

r = session.get(URL)
r.html.render(sleep=1)



#print(r.status_code)

#class Client(QWebEnginePage):
#    def __init__(self, url):
#        self.app = QGuiApplication(sys.argv)
#        QWebPage.__init__(self)
#        self.loadFinished.connect(self.on_page_load)

