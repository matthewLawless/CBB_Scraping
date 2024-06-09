import mysql.connector
import datetime
from datetime import datetime

cbb_betting_lines = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "GodDid",
    database = "cbb_betting_lines",
)

cursor = cbb_betting_lines.cursor()
cursor.execute("SELECT * FROM moneyline")
ans = cursor.fetchall()

for i in ans:
    print(i)

#date = datetime.date(2024, 6, 9)
date = datetime.now()
#date = strftime(date)
print(date)

# cursor.execute(("""INSERT INTO moneyline(date) 
#                             VALUES ('2012-10-03')"""))
cursor.execute("""UPDATE moneyline
                SET home = "MSU", away = "UAB"
                WHERE id = 7""")
cbb_betting_lines.commit()