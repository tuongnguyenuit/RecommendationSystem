import json

from pip._internal.utils import encoding
from py2neo import Graph, authenticate

# replace 'foobar' with your password
authenticate("localhost:7474", "neo4j", "123456")
graph = Graph()
data = []
with open('VungTau.json', encoding='utf8') as data_file:
    json = json.load(data_file)
for i in json:
    print(i["category"])

print(json)
query = """
WITH {json} AS document
UNWIND document.categories AS category
MERGE (:CrimeCategory {name: category.name})
"""

#print (graph.run(query, json = json))