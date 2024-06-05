import bs4
import requests
from requests_html import HTMLSession
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage

fake_URL = "https://realpython.github.io/fake-jobs/"
URL = "https://www.vegasinsider.com/college-basketball/odds/las-vegas/"

fake_Page = requests.get(fake_URL)
page = requests.get(URL)

print(fake_Page.text)
print("====================")
session = HTMLSession()

r = session.get(URL)
r.html.render(sleep=1)

print(r.status_code)

#class Client(QWebEnginePage):
#    def __init__(self, url):
#        self.app = QGuiApplication(sys.argv)
#        QWebPage.__init__(self)
#        self.loadFinished.connect(self.on_page_load)

