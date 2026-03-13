from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.exceptions import BlogException
from blog.models import Post
from blog.serializers.post_serializers import PostDetailSerializer, PostListSerializer
from blog.util.request_parser import get_query_string_filter


class PostPagination(PageNumberPagination):
    page_size = 6


class PostDetailView(APIView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class PostListView(APIView):

    def get(self, request):
        filters = get_query_string_filter(request, "category_id")
        try:
            posts = (
                Post.objects.select_related("category")
                .filter(**filters)
                .order_by("-created_at")
            )
        except ValueError:
            raise BlogException("query string의 타입이 올바르지 않습니다.")

        pagination = PostPagination()
        paginated_posts = pagination.paginate_queryset(posts, request)
        serializer = PostListSerializer(paginated_posts, many=True)
        return pagination.get_paginated_response(serializer.data)
