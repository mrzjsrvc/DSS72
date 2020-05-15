import db
from db import run_sql_string as rsql
# from datetime import datetime
# from datetime import timedelta
# date_string = "17:00"
# format = "%H:%M"
# res = datetime.strptime(date_string, format)
# value = (res.hour*60) + (res.minute)
# print(value)
#
# print(str(timedelta(minutes=value)))

q = int(rsql("SELECT SUM(demand) FROM customers;")[0][0])
print(q)

nr = 20
for i in range(nr):
    if i:
        print("Yes",i)
    else:
        print("No",i)


#db.init()
# a = [1,2,3,4,5]
# b = [3,4,5,6,7]
# c = [6,7]
# d = [8,9]
#
# c, d += a, b
#
# print(c)
# print(d)
