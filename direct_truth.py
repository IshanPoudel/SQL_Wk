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



#Direct truths only 
#Stores Q30-P30-Q31
query = "INSERT INTO direct_truth_triple(entity, property, value) SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), SUBSTRING(predicate, LENGTH('http://www.wikidata.org/prop/direct/') + 1), SUBSTRING(object, LENGTH('<http://www.wikidata.org/entity/') + 1) FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Q[0-9]*' AND predicate REGEXP 'http://www.wikidata.org/prop/direct/P' AND object REGEXP '^<http://www.wikidata.org/entity/Q[0-9]*';"
mycursor.execute(query)

#Stores the entity , property and statement node
#Stores Q30-P30-Q39329400292
query = "INSERT INTO entity_property_statement_triple(entity, property, statement_entity) SELECT SUBSTRING(subject, LENGTH('http://www.wikidata.org/entity/') + 1), SUBSTRING(predicate, LENGTH('http://www.wikidata.org/prop/') + 1), SUBSTRING(object, LENGTH('<http://www.wikidata.org/entity/statement/') + 1) FROM master_table WHERE subject REGEXP '^http://www.wikidata.org/entity/Q[0-9]*' AND predicate REGEXP 'http://www.wikidata.org/prop/P';"
mycursor.execute(query)

db.commit()


