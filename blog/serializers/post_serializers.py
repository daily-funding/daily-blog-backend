from rest_framework import relations
from rest_framework import serializers

from blog.models import Post

# TODO preview_image url로 만들기
class PostDetailSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField(source="id")
    category_name = relations.SlugRelatedField(
        source="category",
        slug_field="name",
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "post_id",
            "category_name",
            "title",
            "subtitle",
            "content",
            "preview_image",
        ]
