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