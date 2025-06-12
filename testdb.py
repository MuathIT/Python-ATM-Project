import sqlite3

db = sqlite3.connect("ATM.db")
cur = db.cursor()
cur.execute("SELECT * FROM users")
data = cur.fetchall()
counter = 1
for row in data:
    print(f"\nUser #{counter}:")
    print("ID:", row[0])
    print("Name:", row[1])
    print("Age:", row[2])
    print("Username:", row[3])
    print("Password:", row[4])
    print("Account number:", row[5])
    print("Balance:", row[6])
    counter+=1

db.commit()
db.close()