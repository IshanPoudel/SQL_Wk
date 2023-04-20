#Read all the lines

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

mycursor.execute("CREATE TABLE one_line (line TEXT)")
db.commit()

with open("general_sample_file.txt", 'r') as f , open("output.txt", 'w') as out_file:
    count =0
    for line in f:
        
        # insert values into the master_table
        sql_query = "INSERT INTO one_line (line) VALUES (%s)"

        mycursor.execute(sql_query , (line,))

db.commit()

mycursor.execute("CREATE TABLE master_table (subject VARCHAR(2000), predicate VARCHAR(2000), object VARCHAR(2000))")

mycursor.execute(""" INSERT INTO master_table (subject, predicate, object)
SELECT TRIM(BOTH '<' FROM SUBSTRING_INDEX(line, '>', 1)) AS subject,
       SUBSTRING_INDEX(SUBSTRING_INDEX(line, '>', 2), '<', -1) AS predicate,
       CASE
           WHEN line LIKE '<%' THEN CONCAT('<', SUBSTRING_INDEX(SUBSTRING_INDEX(line, '>', 2), '<', -1), '>')
           ELSE SUBSTRING_INDEX(line, '>', -1)
       END AS object
FROM one_line""")

db.commit()

