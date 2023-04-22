#just pure mysql queries 
import mysql.connector
from rdflib import Graph, URIRef
import re

import json

f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata_pure_sql")
mycursor = db.cursor()

# mycursor.execute("CREATE TABLE entities_dcp_only(entity VARCHAR(30) , description VARCHAR(500) )")
# mycursor.execute("CREATE TABLE property_dcp_only(property VARCHAR(30) , description VARCHAR(500) )")

# mycursor.execute("CREATE TABLE entities_name_only(entity VARCHAR(30) , name VARCHAR(500) )")
# mycursor.execute("CREATE TABLE property_name_only(property VARCHAR(30) , name VARCHAR(500) )")


#Stores entity id and name and description
#Q30-"Queen Elizabeth"
query = """INSERT INTO entities_name_only(entity, name) SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Q[0-9]*' AND predicate REGEXP 'http://schema.org/name' AND object LIKE '%"@en %.'  """
mycursor.execute(query)

#Stores property id and name
#P31-"Monarch of"
query = """INSERT INTO property_name_only(property, name) SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/P[0-9]*' AND predicate REGEXP 'http://schema.org/name' AND object LIKE  '%"@en %.' """
mycursor.execute(query)

#Stores entity id and description
#Q31-"Queen Elizabeth was the ...."
query = """INSERT INTO entities_dcp_only(entity, description) SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Q[0-9]*' AND predicate REGEXP 'http://schema.org/description' AND object LIKE  '%"@en %.' """
mycursor.execute(query)

#Stores property id and description
#P31-"Relates to the king/queen of ....."

query = """INSERT INTO property_dcp_only(property, description) SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/P[0-9]*' AND predicate REGEXP 'http://schema.org/description' AND object LIKE '%"@en %.' """
mycursor.execute(query)

db.commit()




# INSERT INTO entities_name_only(entity , name)
#  SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), 
# SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE 
# subject REGEXP '^http://www.wikidata.org/entity/Q[0-9]*' AND
#  predicate REGEXP 'http://schema.org/name' AND 
# object LIKE '%"@en %.' ;

#Sotre property p31-Name
# Insert into property_name_only(property , name)
#  SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), 
# SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE 
# subject REGEXP '^http://www.wikidata.org/entity/P[0-9]*' AND
#  predicate REGEXP 'http://schema.org/name' AND 
# object LIKE '%"@en %.'  ;




#Insert entity_description

# Problem with regex timeput/
# INSERT INTO entities_dcp_only(entity , description)
# SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), 
#  SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE  
# subject REGEXP '^http://www.wikidata.org/entity/Q[0-9]*' AND  
# predicate REGEXP 'http://schema.org/description' AND  
# object LIKE '%"@en %.'  ;


#Insert property_description




# INSERT INTO property_dcp_only(property , description)
# SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), 
#  SUBSTRING_INDEX(object, '@en', 1) FROM master_table WHERE  
# subject REGEXP '^http://www.wikidata.org/entity/P[0-9]*' AND  
# predicate REGEXP 'http://schema.org/description' AND  
# object LIKE '%"@en %.' ;


# SELECT 
#     CASE 
#         WHEN object LIKE '"%"@en' THEN SUBSTR(object, 2, LENGTH(object) - 6)
#         WHEN object LIKE '"%"' THEN SUBSTR(object, 2, LENGTH(object) - 2)
#         ELSE object
#     END AS value
# FROM 
#     your_table_name
# WHERE 
#     object LIKE '"%"@en' OR object LIKE '"%"'

