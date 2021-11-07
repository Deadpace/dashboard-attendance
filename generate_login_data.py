import pymongo
import bcrypt

DEFAULT_CONNECTION_URL = "mongodb://localhost:27017/"
DB_NAME= "Login-Database"
client = pymongo.MongoClient(DEFAULT_CONNECTION_URL)
dataBase = client[DB_NAME]

names = ["Rishabh","Jaspreet","Kartik","Dheeraj","Usha","Sonia","Ramesh","Suresh","Priyanka","Pavani"]
email = [f"{name.lower()}@attendance.com" for name in names]
password = "1234" #change password
password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

admin_users_list = ['Rishabh','Jaspreet','Kartik']

collection = dataBase["Login"]
for i in range(len(names)):
    if names[i] in admin_users_list:
        role = "Admin"
    else:
        role = "User"
    record = {"_id":i+1,"Name":names[i],"Email":email[i],"Password":password,"Role":role}
    print(record)
    collection.insert_one(record)