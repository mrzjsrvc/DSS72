# PREREQUISITES:
# https://www.apachefriends.org/index.html  Install Apache XAMPP
# https://pypi.org/project/SQLAlchemy/      Install SQLAlchemy

from __future__ import print_function
import db

var = db.run_sql_string("SELECT longitude FROM customers;")
for x in var:
    print(x)
    
var = db.run_sql_string("SELECT * FROM vehicles;")
for x in var:
    print(x)
    
    
print("\n","TYPE: ",type(var))
