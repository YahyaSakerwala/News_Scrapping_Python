import json
from elasticsearch import Elasticsearch
from scrapeFunctionsModule import ap_news,asahi_news,investing_news


# ELASTIC_PASSWORD = "OMddL2qDGNJinws6DnNq"
api_key="MlA2TGdZd0JNVTh6OHZHdFhBRWw6TWI1WjdSQS1UVWFLenh4ZThzdF92QQ=="

client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="C:\\Users\\3439\\Elastic-Kibana\\kibana-8.11.3\\data\\ca_1702534907563.crt",
    # basic_auth=("elastic", ELASTIC_PASSWORD)
    api_key=api_key
)

print(client.ping())

json_objects=[]

if __name__ == "__main__":
   ap_news.scrape_ap_news()
   asahi_news.scrape_asahi_news()
   investing_news.scrape_investing_news()

with open("data/ap_news.json","r") as f:
    data1 = json.load(f)
    f.close() 

with open("data/asahi_news.json","r") as f:
    data2 = json.load(f)
    f.close() 

with open("data/investing_news.json","r") as f:
    data3 = json.load(f)
    f.close() 

# Combine the arrays into a single list
combined_objects_array= data1 + data2 + data3

client.indices.create(index="news")
for combined_object in combined_objects_array:
    doc_id=combined_object['url']
    response=client.index(index="news",body=combined_object,id=doc_id)
    
