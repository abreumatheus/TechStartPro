from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter]
    search_fields = ['name']

    pagination_class = PageNumberPagination
    pagination_class.page_size = 100
