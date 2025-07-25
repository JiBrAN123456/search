from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")

def is_connected():
    return es.ping()
