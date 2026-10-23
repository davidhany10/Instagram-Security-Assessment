import MySQLdb
from werkzeug.security import generate_password_hash

db = MySQLdb.connect(host="localhost", user="root", password="102030", db="instagram_clone")
cursor = db.cursor()

email = input("Enter email: ")
new_password = input("Enter new password: ")

hashed = generate_password_hash(new_password)

cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed, email))
db.commit()
print("Password updated.")
db.close()
