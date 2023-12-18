import json
from elasticsearch import Elasticsearch
from scrapeFunctionsModule import ap_news,asahi_news

ELASTIC_PASSWORD = "OMddL2qDGNJinws6DnNq"

client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="C:\\Users\\3439\\Elastic-Kibana\\kibana-8.11.3\\data\\ca_1702534907563.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

print(client.ping())

if __name__ == "__main__":
   ap_news.scrape_ap_news()
   asahi_news.scrape_asahi_news()

with open("data/ap_news.json","r") as f:
    json_objects = json.load(f)
    f.close() 

for json_doc in json_objects:
    doc_id=json_doc['url']
    response = client.index(index="ap_news", body=json_doc, id=doc_id)

with open("data/asahi_news.json","r") as f:
    json_objects = json.load(f)
    f.close() 
 
for json_doc in json_objects:
    doc_id=json_doc['url']
    response = client.index(index="asahi_news", body=json_doc, id=doc_id)