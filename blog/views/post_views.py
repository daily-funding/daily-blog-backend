from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from blog.paginations.PostPagination import PostPagination
from blog.serializers.post_serializers import PostDetailSerializer, PostListSerializer

class PostDetailView(APIView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class PostListView(APIView):

    def get(self, request):
        filters = {
            key: value
            for key, value in request.query_params.items()
            if key in ["category_id"]
        }
        posts = Post.objects.filter(**filters).order_by("-created_at")
        pagination = PostPagination()
        paginated_posts = pagination.paginate_queryset(posts, request)
        serializer = PostListSerializer(paginated_posts, many=True)
        return pagination.get_paginated_response(serializer.data)
