from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers.post_serializers import PostDetailSerializer


class PostView(APIView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
