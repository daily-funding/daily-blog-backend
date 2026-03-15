from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Category
from blog.serializers.category_serializers import CategoryListSerializer


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response({"categories": serializer.data})
