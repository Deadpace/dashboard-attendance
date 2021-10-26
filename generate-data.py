import pymongo
import random
import datetime
random.seed(15)

DEFAULT_CONNECTION_URL = "mongodb://localhost:27017/"
DB_NAME= "Attendance"
client = pymongo.MongoClient(DEFAULT_CONNECTION_URL)
dataBase = client[DB_NAME]

no_of_days = 30
for i in range(1,no_of_days+1):
    date = datetime.date(2021,9,i)
    coll_date = date.strftime("%Y-%m-%d")
    rand_num = random.randint(6,10)
    collection = dataBase[f"Attendance_{coll_date}"]
    name = random.sample(["Rishabh","Jaspreet","Kartik","Dheeraj","Usha","Sonia","Ramesh","Suresh","Priyanka","Pavani"],rand_num)
    for j in range(rand_num):
        check_in_time = datetime.datetime(2021,10,i,9,0)+datetime.timedelta(minutes=random.randrange(60))
        check_out_time = datetime.datetime(2021,10,i,7,0)+datetime.timedelta(minutes=random.randrange(60))
        record = {"_id": j+1,
            'Name': name[j],
             'Time': check_in_time.strftime("%H:%M:%S"),
             'Date': date.strftime("%d/%m/%Y"),
             "Check_In":1,
             "Check Out":1,
             "Check Out Time":check_out_time.strftime("%H:%M:%S")
                 }
        print(record)
        collection.insert_one(record)
    print(end = "\n\n")