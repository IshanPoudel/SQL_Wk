import mysql.connector

import re
import json
import time




f = open('database_config.json')
data = json.load(f)

db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'])

mycursor = db.cursor()

mycursor.execute("DROP database if exists wikidata_pure_sql ")
mycursor.execute("CREATE database wikidata_pure_sql")





db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata_pure_sql")

mycursor = db.cursor()

mycursor.execute("CREATE TABLE master_table (subject VARCHAR(2000), predicate VARCHAR(2000), object VARCHAR(2000))")

db.commit()

start_time = time.time()


mycursor.execute("""LOAD DATA  INFILE '/Users/user/Desktop/Wikidata_Refactored/Wikipedia_Refactored_pure_sql/small_sample.txt' INTO TABLE master_table FIELDS TERMINATED BY '>' LINES TERMINATED BY '\n' (@subject, @predicate, @object)
SET subject = TRIM(BOTH '<' FROM SUBSTRING_INDEX(@subject, '<', -1)),predicate = SUBSTRING_INDEX(@predicate, '<', -1),object = CASE WHEN @object LIKE '<%' THEN CONCAT('<', SUBSTRING_INDEX(@object, '>', 1), '>') ELSE @object END""")
                 

db.commit()
end_time = time.time()

print("Elapsed time: ", end_time - start_time, "seconds")

mycursor.close()
db.close()
