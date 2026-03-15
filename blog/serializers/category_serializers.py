from rest_framework import serializers

from blog.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Category
        fields = ["category_id", "name"]
