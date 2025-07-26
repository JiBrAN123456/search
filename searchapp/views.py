from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer
from django.db import models


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='simple-search')
    def simple_search(self, request):

        query = request.query_params.get('q', '')

        if query:
            products = Product.objects.filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )
        else:
            products = Product.objects.none()

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='es-search')
    def es_search(self, request):
        from elasticsearch import Elasticsearch

        query = request.query_params.get('q', '')
        es = Elasticsearch("http://localhost:9200")

        if not query:
           return Response([])

        res = es.search(index="products", body={
            "query": {
               "multi_match": {
                "query": query,
                "fields": ["name", "description", "category"],
                "fuzziness": "AUTO"
                }
           }
        })

        hits = [hit["_source"] for hit in res["hits"]["hits"]]
        return Response(hits)

