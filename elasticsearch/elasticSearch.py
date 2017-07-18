#-*-coding:utf8-*-

import requests
import traceback
from datetime import datetime
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
req = requests.get('http://localhost:9200')

def IndexData(filename):
    """
    FileName where data exists and to be indexed to Elastic Search
    :param filename: 
    :return: nothing; index data in Elastic search server
    """
    fileAsArray = open(filename, "r").read().splitlines()
    for eachlineNo in range(1,len(fileAsArray)): # as first line is header, omitted
        try:
            # Zipcode,ZipCodeType,City,State,LocationType,Lat,Long,Location,Decommisioned,TaxReturnsFiled,EstimatedPopulation,TotalWages
            print "Processing Line : ", eachlineNo
            Zipcode,ZipCodeType,City,State,LocationType,Lat,Long,Location,Decommisioned,TaxReturnsFiled,EstimatedPopulation,TotalWages = fileAsArray[eachlineNo].split(",")
            es.index(index='usa-index', doc_type='usa', id=eachlineNo, body={'Zipcode':Zipcode,'City': City, 'State': State, 'Lat': Lat, 'Long': Long})
        except:
            print "Some Error Exist at Line : ",eachlineNo



def searchESforZipcode(zipcode):
    queryResult = es.search(index='usa-index', body={"query": {"fuzzy": {'Zipcode':zipcode }}})
    if queryResult['hits']['total'] >= 1:
        return queryResult['hits']['hits'][0]['_source']
    else:
        return False


# to index data in Elastic Search
# IndexData("free-zipcode-database-Primary.csv")
#Query data
print (searchESforZipcode(611))
