from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]