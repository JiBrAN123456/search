from elasticsearch import Elasticsearch
from .models import Product

es = Elasticsearch("http://localhost:9200")

def index_product(product):
    doc = {
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": float(product.price),
        "suggest": {
            "input": [product.name, product.category]
        }
        # Add other fields like city, available_dates, etc.
    }
    es.index(index="products", id=product.id, body=doc)

