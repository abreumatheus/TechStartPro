from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
