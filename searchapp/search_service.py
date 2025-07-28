from elasticsearch import Elasticsearch
from .models import Product

es = Elasticsearch("http://localhost:9200")

def index_product(product):
    available_dates = list(
        product.slots.filter(is_available=True)
        .values_list('date', flat=True)
        .distinct()
    )

    doc = {
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": float(product.price),
        "available_dates": [str(date) for date in available_dates],
        "suggest": {
            "input": [product.name, product.category]
        }
    }

    es.index(index="products", id=product.id, body=doc)


