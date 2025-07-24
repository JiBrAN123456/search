from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from django.db import models


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
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
