from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers.post_serializers import PostDetailSerializer, PostListSerializer

class PostDetailView(APIView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class PostListView(APIView):

    def get(self, request):
        pagination = PageNumberPagination()
        posts = pagination.paginate_queryset(Post.objects.all(), request)
        serializer = PostListSerializer(posts, many=True)
        return pagination.get_paginated_response(serializer.data)
