import mysql.connector
import datetime
from datetime import datetime
from sql_creds import Credentials
import datetime


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

dateT = datetime.date(2024, 6, 9)
#date = datetime.now()
#date = strftime(date)
print(str(dateT))

# cursor.execute("""DELETE FROM moneyline WHERE date = '2023-11-07' """)
cursor.execute("SELECT COUNT(*) FROM moneyline")
ans = cursor.fetchall()
#print(ans)
cbb_betting_lines.commit()