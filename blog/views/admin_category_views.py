import logging
from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.db import IntegrityError, transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from blog.models import Category, Post

MAX_CATEGORY_COUNT = 12
logger = logging.getLogger(__name__)


def admin_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url="admin:login")

        if not request.user.is_staff:
            return redirect_to_login(request.get_full_path(), login_url="admin:login")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def _is_ajax_request(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


@admin_access_required
def admin_category_manage_view(request):
    categories = Category.objects.annotate(post_count=Count("post")).order_by(
        "created_at"
    )

    return render(
        request,
        "blog/admin/category_manage.html",
        {"categories": categories},
    )


@admin_access_required
@require_POST
def admin_category_create_view(request):
    name = request.POST.get("name", "").strip()

    if not name:
        if _is_ajax_request(request):
            return JsonResponse(
                {"message": "카테고리 이름을 입력해주세요."}, status=400
            )
        messages.error(request, "카테고리 이름을 입력해주세요.")
        return redirect("blog:admin-category-manage")

    if Category.objects.filter(name__iexact=name).exists():
        if _is_ajax_request(request):
            return JsonResponse(
                {"message": "이미 존재하는 카테고리입니다."}, status=400
            )
        messages.error(request, "이미 존재하는 카테고리입니다.")
        return redirect("blog:admin-category-manage")

    if Category.objects.count() >= MAX_CATEGORY_COUNT:
        if _is_ajax_request(request):
            return JsonResponse(
                {
                    "message": f"카테고리는 최대 {MAX_CATEGORY_COUNT}개까지 생성할 수 있습니다."
                },
                status=400,
            )
        messages.error(
            request, f"카테고리는 최대 {MAX_CATEGORY_COUNT}개까지 생성할 수 있습니다."
        )
        return redirect("blog:admin-category-manage")

    try:
        with transaction.atomic():
            category = Category.objects.create(name=name)
    except IntegrityError:
        logger.warning("Duplicate category creation blocked: %s", name)
        if _is_ajax_request(request):
            return JsonResponse(
                {"message": "이미 존재하는 카테고리입니다."}, status=400
            )
        messages.error(request, "이미 존재하는 카테고리입니다.")
        return redirect("blog:admin-category-manage")

    if _is_ajax_request(request):
        return JsonResponse(
            {
                "message": "카테고리가 추가되었습니다.",
                "category": {
                    "id": category.id,
                    "name": category.name,
                    "post_count": 0,
                    "created_at": category.created_at.strftime("%Y-%m-%d"),
                },
            }
        )

    messages.success(request, "카테고리를 생성했습니다.")
    return redirect("blog:admin-category-manage")


@admin_access_required
@require_POST
def admin_category_delete_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if Post.objects.filter(category=category).exists():
        if _is_ajax_request(request):
            return JsonResponse(
                {
                    "message": "해당 카테고리를 사용하는 게시물이 존재하여 삭제할 수 없습니다."
                },
                status=400,
            )
        messages.error(
            request, "해당 카테고리를 사용하는 게시물이 존재하여 삭제할 수 없습니다."
        )
        return redirect("blog:admin-category-manage")

    category.delete()

    if _is_ajax_request(request):
        return JsonResponse({"message": "카테고리가 삭제되었습니다."})

    messages.success(request, "카테고리를 삭제했습니다.")
    return redirect("blog:admin-category-manage")
