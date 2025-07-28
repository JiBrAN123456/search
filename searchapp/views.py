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
            es = Elasticsearch("http://localhost:9200")
    
            q = request.query_params.get("q", "")
            category = request.query_params.get("category")
            price_min = request.query_params.get("price_min")
            price_max = request.query_params.get("price_max")
            date = request.query_params.get("date")

            must = []
            filter_ = []

            if q:
               must.append({
            "multi_match": {
                "query": q,
                "fields": ["name", "description", "category"],
                "fuzziness": "AUTO"
            }
            })

            if category:
               filter_.append({"term": {"category": category.lower()}})

            if date:
               filter_.append({"term": {"available_dates": date}})   

            if price_min:
               filter_.append({"range": {"price": {"gte": float(price_min)}}})

            if price_max:
               filter_.append({"range": {"price": {"lte": float(price_max)}}})

            body = {
                  "query": {
                      "bool": {
                         "must": must,
                            "filter": filter_
                        }
                      }
                  }

            res = es.search(index="products", body=body)
            return Response([hit["_source"] for hit in res["hits"]["hits"]])


