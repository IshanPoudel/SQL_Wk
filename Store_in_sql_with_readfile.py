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

with open("general_sample_file.txt", 'r') as f , open("output.txt", 'w') as out_file:
    count =0
    for line in f:
        values = re.findall(r'<([^>]*)>', line)
        parts = line.split('>')
        third_part = parts[2].strip()

        # insert values into the master_table
        sql = "INSERT INTO master_table (subject, predicate, object) VALUES (%s, %s, %s)"
        val = (values[0], values[1], third_part)
        mycursor.execute(sql, val)
        db.commit()
        count=count+1
        if count % 10000 == 0 :
            print(count)

        # print(values[0], values[1], third_part)
        out_file.write(f"{values[0]}\t{values[1]}\t{third_part}\n")

end_time = time.time()

print("Elapsed time: ", end_time - start_time, "seconds")
# Format stuff to other file. 


mycursor.close()
db.close()

# LOAD DATA INFILE 'general_sample_file.txt' INTO TABLE master_table FIELDS TERMINATED BY '>' 
# LINES TERMINATED BY '\n' (@subject, @predicate, @object)
# SET subject = TRIM(BOTH '<' FROM SUBSTRING_INDEX(@subject, '<', -1)),
# predicate = SUBSTRING_INDEX(@predicate, '<', -1),
# object = CASE
#     WHEN @object LIKE '<%' THEN CONCAT('<', SUBSTRING_INDEX(@object, '>', 1), '>')
#     ELSE @object
#     END;


# mycursor.execute("""LOAD DATA INFILE 'general_sample_file.txt' INTO TABLE master_table FIELDS TERMINATED BY '>' LINES TERMINATED BY '\n' (@subject, @predicate, @object)
# SET subject = TRIM(BOTH '<' FROM SUBSTRING_INDEX(@subject, '<', -1)),predicate = SUBSTRING_INDEX(@predicate, '<', -1),object = CASE WHEN @object LIKE '<%' THEN CONCAT('<', SUBSTRING_INDEX(@object, '>', 1), '>') ELSE @object END""")
                 

# db.commit()
