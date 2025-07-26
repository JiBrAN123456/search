from elasticsearch import Elasticsearch
from .models import Product

es = Elasticsearch("http://localhost:9200")

def index_product(product):
    doc = {
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": float(product.price)
    }
    es.index(index="products", id=product.id, body=doc)

def delete_product(product_id):
    es.delete(index="products", id=product_id, ignore=[404])
