import mysql.connector
import datetime
from datetime import datetime
from sql_creds import Credentials


cbb_betting_lines = mysql.connector.connect(
    host =  (Credentials.host).value,
    user =  (Credentials.user).value,
    password = (Credentials.password).value,
    database = (Credentials.database.value),
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

cursor.execute("""INSERT INTO moneyline (home, away, date, bookmaker)
                                    VALUES('ILL', 'ISU', '2024-03-25', 'DRAFTKINGS')
                                    ON DUPLICATE KEY UPDATE
                                    home = 'AL'""")
cbb_betting_lines.commit()