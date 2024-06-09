import mysql.connector

cbb_betting_lines = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "GodDid",
    database = "cbb_betting_lines",
)

cursor = cbb_betting_lines.cursor()
cursor.execute("SELECT date FROM moneyline")