import pymysql as mdb
from datetime import datetime,timedelta
import math

mdb.install_as_MySQLdb()

mysql_host = "localhost"
mysql_user = "precosky_fridge"
mysql_passwd = "fridge"
mysql_db = "fridge_db"

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta




if __name__ == "__main__":

    conn = mdb.connect(host=mysql_host, user=mysql_user, password=mysql_passwd, db=mysql_db)
    cursor = conn.cursor()
 
    start_time = datetime.now() - timedelta(days=1)
    end_time = datetime.now()

    for i, the_time in enumerate(perdelta( start_time, end_time, timedelta(seconds=10))):
        insert_temperature = math.sin(2*3.14*i/360.0) + 2.5
        insert_voltage = 4.2

        insert_stmt = ("INSERT INTO fridge (time, temperature, batteryVoltage) VALUES (%s, %s, %s)")        
        data = (the_time, str(insert_temperature), str(insert_voltage))
    
        cursor.execute(insert_stmt, data)
