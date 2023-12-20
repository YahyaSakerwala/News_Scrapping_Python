# # client.info()
# print(client.ping())

# # creating a index 
# client.indices.create(index="asahi_news")



# # creating a index 
# client.indices.create(index="ap_news")

# es = Elasticsearch(
#         ['https://localhost:9200'],
#         use_ssl=True,
#         verify_certs=True,
#         ca_certs=os.path.join('path/to/your/kibana/data/folder', 'ca_1702548513853.crt')
#     )


# if __name__ == "__main__":
#     scrape_apnews_data()


import json
from selenium.webdriver.support import expected_conditions as EC
from elasticsearch import Elasticsearch

ELASTIC_PASSWORD = "OMddL2qDGNJinws6DnNq"

client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="C:\\Users\\3439\\Elastic-Kibana\\kibana-8.11.3\\data\\ca_1702534907563.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)
print(client.ping())





# for json_doc in json_objects:
#     doc_id=json_doc['url']
#     response = client.index(index="ap_news", body=json_doc, id=doc_id)


# for json_doc in json_objects:
#     doc_id=json_doc['url']
#     response = client.index(index="asahi_news", body=json_doc, id=doc_id)

 
# for json_doc in json_objects:
#     doc_id=json_doc['url']
#     response = client.index(index="investing_news", body=json_doc, id=doc_id)








# class_ = value['class'].split() if 'class' in value else None
#                     attributes = {}
#                     if 'attributes' in value and isinstance(value['attributes'], dict):
#                         attributes = {attr_key: attr_value for attr_key, attr_value in value['attributes'].items()}
#                     key_element = soup.find(tag, class_=class_, attrs=attributes)
#                     metadata[key] = key_element.text.strip() if key_element else None