from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('category', views.CategoryViewSet, basename='category')
router.register('product', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]