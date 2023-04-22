#just pure mysql queries 

import mysql.connector
import re
import json

f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata_pure_sql")

mycursor = db.cursor()


#Stores entities
#Store Q344003032-P30-Q30
query = "INSERT INTO statement_triple(entity, property, statement) SELECT SUBSTRING(subject, LOCATE('statement/', subject) + LENGTH('statement/')) AS subject_part, SUBSTRING(predicate, LOCATE('http://www.wikidata.org/', predicate) + LENGTH('http://www.wikidata.org/')) AS predicate_part, CONCAT('<entity>', SUBSTRING(object, LOCATE('<http://www.wikidata.org/entity/', object) + LENGTH('<http://www.wikidata.org/entity/'))) AS object_part FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/statement/P' and object REGEXP '<http://www.wikidata.org/entity/Q';"
mycursor.execute(query)


#Stores simple string
#Q3440003-P30-"Queen Elizabeth"  
sqlquery = """INSERT INTO statement_triple (entity, property, statement)
              SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, 
              SUBSTRING(predicate, LOCATE("http://www.wikidata.org/", predicate) + LENGTH("http://www.wikidata.org/")) AS predicate_part, 
              SUBSTRING(object, LOCATE('"', object) + 1, LOCATE('"', object, LOCATE('"', object) + 1) - LOCATE('"', object) - 1) AS object_part
              FROM master_table 
              WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' 
              and predicate REGEXP 'http://www.wikidata.org/prop/statement/P' and 
              object REGEXP '^"[^"]*"(@en)?[[:space:]]*\.$'"""

mycursor.execute(sqlquery)



#Stores custom wikidata types
#Q34000303-P30-<Latitude>(30.449 , 23.2393)
mycursor.execute("INSERT INTO statement_triple (entity, property, statement) SELECT SUBSTRING(subject, LOCATE('statement/', subject) + LENGTH('statement/')) AS subject_part, SUBSTRING(predicate, LOCATE('http://www.wikidata.org/', predicate) + LENGTH('http://www.wikidata.org/')) AS predicate_part, CONCAT('<', SUBSTRING_INDEX(object, '#', -1), '> ', TRIM(BOTH '\"' FROM SUBSTRING_INDEX(object, '\"^^', 1))) AS formatted_object FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' AND predicate REGEXP 'http://www.wikidata.org/prop/statement/P' AND (object LIKE '%/XMLSchema#%' OR object LIKE '%geosparql#wktLite%')")





#Stores vale node
#ca2700000d0d0  represents the value index
#Q43043040-P30-ca2700000d0d0 
query = """ INSERT INTO statement_triple (entity, property, statement) SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , SUBSTRING(object, LOCATE("<http://www.wikidata.org/value/", object) + LENGTH("<http://www.wikidata.org/value/")) AS object_part  FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/statement/value/P' and  object REGEXP '<http://www.wikidata.org/value/'"""
mycursor.execute(query)


#Sotres qualifiers value nodes
#Q340400203-qualifier/P30-ca2700000d0d0 
query = """ INSERT INTO statement_triple (entity, property, statement) SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , SUBSTRING(object, LOCATE("<http://www.wikidata.org/value/", object) + LENGTH("<http://www.wikidata.org/value/")) AS object_part  FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/qualifier/value/P' and  object REGEXP '<http://www.wikidata.org/value/'"""
mycursor.execute(query)


#Stores qualifiers entity
# Q34004030-qualifer/P31-Q34
query = """ INSERT INTO statement_triple (entity, property, statement) SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , CONCAT('<entity>', SUBSTRING(object, LOCATE("<http://www.wikidata.org/entity/", object) + LENGTH("<http://www.wikidata.org/entity/"))) AS object_part  FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/qualifier/P'  and object REGEXP '<http://www.wikidata.org/entity/Q'"""
mycursor.execute(query)


#Stores qualifier simple string
#Q3440003-qualifier/P31-"Monarch of England"  
query = """ INSERT INTO statement_triple (entity, property, statement) SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , SUBSTRING(object, LOCATE('"', object) + 1, LOCATE('"', object, LOCATE('"', object) + 1) - LOCATE('"', object) - 1) AS object_part FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/qualifier/P'  and object REGEXP '^"[^"]*"(@en)?[[:space:]]*\.$'"""
mycursor.execute(query)

#Stores custom wikidata types for qualifiers
#Q34000303-qualifier/P30-<Latitude>(30.449 , 23.2393)
query = """INSERT INTO statement_triple (entity, property, statement) SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,  SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , CONCAT('<', SUBSTRING_INDEX(object, '#', -1), '> ', TRIM(BOTH '"' FROM SUBSTRING_INDEX(object, '"^^', 1))) AS formatted_object FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/qualifier/P'  and object LIKE '%/XMLSchema#%' OR object LIKE '%geosparql#wktLite%' """


mycursor.execute(query)






















#Get all the entities and prop/statemenr and entities


# 1.

#1a grabs entities

# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, 
# SUBSTRING(predicate, LOCATE("http://www.wikidata.org/", predicate) + LENGTH("http://www.wikidata.org/")) AS predicate_part , 
# CONCAT('<entity>', SUBSTRING(object, LOCATE("<http://www.wikidata.org/entity/", object) + LENGTH("<http://www.wikidata.org/entity/"))) AS object_part  
# FROM master_table 
# WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and 
# predicate REGEXP 'http://www.wikidata.org/prop/statement/P' and 
# object REGEXP '<http://www.wikidata.org/entity/Q'
# Gets Q183-D067800 - PROP/STATEMETN/P2340 - <ENTITY>420 . Note that entity is added.

#--------------1b Needs to grab simple string------
#The way to grab the simple string is to look fot " " , or could possibly be stuff ending with " "@9(two-letters)

# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, 
# SUBSTRING(predicate, LOCATE("http://www.wikidata.org/", predicate) + LENGTH("http://www.wikidata.org/")) AS predicate_part , 
# SUBSTRING(object, LOCATE('"', object) + 1, LOCATE('"', object, LOCATE('"', object) + 1) - LOCATE('"', object) - 1) AS object_part 
# FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' 
# and predicate REGEXP 'http://www.wikidata.org/prop/statement/P' and  
# object REGEXP '^"[^"]*"(@en)?[[:space:]]*\.$'

#1c Need to grab wikidata data type
#SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, SUBSTRING(predicate, LOCATE("http://www.wikidata.org/", predicate) + LENGTH("http://www.wikidata.org/")) AS predicate_part , object FROM master_table  WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and  predicate REGEXP 'http://www.wikidata.org/prop/statement/P' and object LIKE '%/XMLSchema#%' OR object LIKE '%geosparql#wktLite%'
# Need to split
# 1c.a grab xmldataschema#
#Done with  < and > 

# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,  
# SUBSTRING(predicate, LOCATE("http://www.wikidata.org/", predicate) + LENGTH("http://www.wikidata.org/")) AS predicate_part ,  
# CONCAT('<', SUBSTRING_INDEX(object, '#', -1), '> ', TRIM(BOTH '"' FROM SUBSTRING_INDEX(object, '"^^', 1))) AS formatted_object 
#  FROM master_table  
# WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and  
# predicate REGEXP 'http://www.wikidata.org/prop/statement/P' and 
# object LIKE '%/XMLSchema#%' OR object LIKE '%geosparql#wktLite%';

# 2. Gets statment/value/p23 -- 4384040840480
# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , SUBSTRING(object, LOCATE("<http://www.wikidata.org/value/", object) + LENGTH("<http://www.wikidata.org/value/")) AS object_part  FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/statement/value/P' and  object REGEXP '<http://www.wikidata.org/value/'

#3. Gets qualifier/value/p23 -- 832082802002802
# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part, SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , SUBSTRING(object, LOCATE("<http://www.wikidata.org/value/", object) + LENGTH("<http://www.wikidata.org/value/")) AS object_part  FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and predicate REGEXP 'http://www.wikidata.org/prop/qualifier/value/P' and  object REGEXP '<http://www.wikidata.org/value/'

#4. Gets qualifier value/statement/data type. 
#4.0 Grab all
# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,
#  SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , 
# object
# FROM master_table 
# WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and 
# predicate REGEXP 'http://www.wikidata.org/prop/qualifier/P' 

#4a grab entities.
# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,
#  SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , 
# CONCAT('<entity>', SUBSTRING(object, LOCATE("<http://www.wikidata.org/entity/", object) + LENGTH("<http://www.wikidata.org/entity/"))) AS object_part  
# FROM master_table 
# WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and 
# predicate REGEXP 'http://www.wikidata.org/prop/qualifier/P'  and
# object REGEXP '<http://www.wikidata.org/entity/Q'

#4b grab simple string
# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,
#  SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , 
# SUBSTRING(object, LOCATE('"', object) + 1, LOCATE('"', object, LOCATE('"', object) + 1) - LOCATE('"', object) - 1) AS object_part 
# FROM master_table 
# WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and 
# predicate REGEXP 'http://www.wikidata.org/prop/qualifier/P'  and
# object REGEXP '^"[^"]*"(@en)?[[:space:]]*\.$'

#4c Grab data schema


# SELECT SUBSTRING(subject, LOCATE("statement/", subject) + LENGTH("statement/")) AS subject_part,  
#  SUBSTRING(predicate, LOCATE("http://www.wikidata.org/prop/", predicate) + LENGTH("http://www.wikidata.org/prop/")) AS predicate_part , 
# CONCAT('<', SUBSTRING_INDEX(object, '#', -1), '> ', TRIM(BOTH '"' FROM SUBSTRING_INDEX(object, '"^^', 1))) AS formatted_object 
#  FROM master_table  
# WHERE subject REGEXP '^http://www.wikidata.org/entity/Statement/Q' and  
# predicate REGEXP 'http://www.wikidata.org/prop/qualifier/P'  and 
# object LIKE '%/XMLSchema#%' OR object LIKE '%geosparql#wktLite%';

#Now get the object
# http://www.wikidata.org/prop/statement/P


db.commit()

