[OUT OF DATE!]

## Preqrequisites
 ---
Install [Apache XAMPP](https://www.apachefriends.org/index.html) (may need restarting computer)

Install [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)

## Usage
 ---
Open XAMPP.
Start MySQL.
Now you can do the following in your code:
```
import db
var = db.run_sql_string("SELECT * FROM customers;")
```
OR
```
from db import run_sql_script as sql
var = sql("SELECT * FROM customers;")
```
It will work for both selecting and inserting. Inserting only returns "_Done_", select returns the query.

In _csv_names_ you list the data files you want to be loaded into the database on start.
They must be in the csv-format, but the extension doesn't matter.
Each of the files must have their columns named above, since they are loaded with pandas, and SQL needs to know which column to put which cell in.
The files must be named after their table so that they are put into the right one.

Do not put insert-statements in the init-file, it can't be parsed in the python code yet. (but we probably won't need inserts)

## Current Tables
 ---
#### Customers
| idx | name | latitude | longitude | demand(in tons) |
| ------ | ------ | ------ | ------ | ------ |
| 0 | Karlshamn | 56.170077 | 14.860848999999998 | 0 |
| 1 | Sölvesborg | 56.052108999999994 | 14.584848000000001 | 10 |
| 2 | Olofström | 56.276964 | 14.530781 | 15 |
| 3 | Ronneby | 56.21005699999999 | 15.276960999999998 | 20 |
| 4 | Karlskrona | 56.161735 | 15.585788 | 25 |

#### Vehicles
| index | brand | capacity | fuel_consumption | 
| ------ | ------ | ------ | ------ |
| 0 | Scania | 5 | 23.7 | 
| 1 | Scania 2 | 15 | 23.7 | 
| 2 | Mercedes | 10 | 29 | 
| 3 | Mercedes | 20 | 29 | 

#### Times
| index | name | minutes |
| ------ | ------ | ------ |
| 0 | loading_time | 10 |
| 1 | unloading_time | 10 |
| 2 | resting_time | 120 |
| 3 | total_work_time | 600 |

#### Goods
This table is empty, but added in case we extend the program later, if we have time


#### Request Handler
At the moment, it receives source and destination from the user, it does a request of a map with all the possible paths from the source to the destination.
