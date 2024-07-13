from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MakeUserAsStaff, MakeUserAsNotStaff, ChangeProductStatus

router = DefaultRouter()

router.register('category', views.CategoryViewSet, basename='category')
router.register('product', views.ProductViewSet, basename='product')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('make-user-as-staff/<int:pk>/', MakeUserAsStaff.as_view(), name='make_user_as_staff'),
    path('make-user-as-not-staff/<int:pk>/', MakeUserAsNotStaff.as_view(), name='make_user_as_not_staff'),
    path('change-product-status/<int:pk>/', ChangeProductStatus.as_view(), name='make_user_as_not_staff'),
    path('', include(router.urls)),
]