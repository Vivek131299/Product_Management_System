from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


@csrf_exempt
def register(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)

        username = request_body['username']
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists", status=409)
        email = request_body['email']

        # validate email
        try:
            validate_email(email)
        except ValidationError as e:
            print(e.message)
            return HttpResponse(f"Invalid email: {username}")

        password = request_body['password']

        User.objects.create_user(username=username, email=email, password=password)
        return HttpResponse(f"User created with username: {username}")


class MakeUserAsStaff(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            if request.user.is_superuser:
                user_to_change = User.objects.get(pk=pk)
                if user_to_change.is_staff:
                    return HttpResponse(f"User {user_to_change.username} is already a staff")
                else:
                    user_to_change.is_staff = True
                    user_to_change.save()
                    return HttpResponse(f"User {user_to_change.username} is now a staff")


class MakeUserAsNotStaff(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            if request.user.is_superuser:
                user_to_change = User.objects.get(pk=pk)
                if user_to_change.is_staff:
                    user_to_change.is_staff = False
                    user_to_change.save()
                    return HttpResponse(f"User {user_to_change.username} is not anymore a staff")
                else:
                    return HttpResponse(f"User {user_to_change.username} is already not a staff")


class ChangeProductStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        if pk:
            if request.user.is_staff:
                product = Product.objects.get(pk=pk)
                request_body = json.loads(request.body)
                product.status = request_body['status']
                product.save()
                return HttpResponse(f"Status of product id={pk} is changed to {request_body['status']}")


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

    def create(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        if 'status' in request_body:
            return HttpResponse("Status should not be provided", status=400)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        if 'status' in request_body:
            return HttpResponse("You cannot update status. Only staff user can update the status.", status=401)
        return super().update(request, *args, **kwargs)