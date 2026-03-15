from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from blog.exceptions import BlogException
from blog.models import Post, Pin
from blog.serializers.post_serializers import (
    PostDetailSerializer,
    PostListSerializer,
    TopPostListSerializer,
)
from blog.util.request_parser import get_query_string_filter


class PostPagination(PageNumberPagination):
    page_size = 6


@api_view(["GET"])
def post_detail(request, post_id):
    """게시물 상세 조회"""
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)


@api_view(["GET"])
def post_list(request):
    """
    페이지 기반 게시물 목록 조회
    Query Params:
        - page (int, optional): 페이지 번호(기본 1)
        - category_id (int, optional): 카테고리 필터
    """
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


@api_view(["GET"])
def top_post_list(request):
    """고정 게시물 목록 조회"""
    pins = Pin.objects.filter(post=OuterRef("id"))
    pinned_posts = (
        Post.objects.select_related("category")
        .annotate(sort_order=Subquery(pins.values("sort_order")[:1]))
        .filter(sort_order__isnull=False)
        .order_by("sort_order")
    )
    serializer = TopPostListSerializer(pinned_posts, many=True)
    return Response(serializer.data)
