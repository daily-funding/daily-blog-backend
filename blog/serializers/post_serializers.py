from rest_framework import relations
from rest_framework import serializers

from blog.models import Post


class PostDetailSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField(source="id")
    category_id = relations.SlugRelatedField(
        source="category",
        slug_field="id",
        read_only=True
    )
    category_name = relations.SlugRelatedField(
        source="category",
        slug_field="name",
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "post_id",
            "category_id",
            "category_name",
            "title",
            "subtitle",
            "content",
            "preview_image",
        ]


class PostListSerializer(serializers.ModelSerializer):

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
            "category_id",
            "category_name",
            "title",
            "description",
            "preview_image",
        ]

class TopPostListSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField(source="id")
    category_id = relations.SlugRelatedField(
        source="category",
        slug_field="id",
        read_only=True
    )
    category_name = relations.SlugRelatedField(
        source="category",
        slug_field="name",
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "post_id",
            "category_id",
            "category_name",
            "title",
            "subtitle",
            "preview_image",
        ]
