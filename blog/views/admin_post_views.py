from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed   
import logging
from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from blog.forms import PostCreateForm
from blog.models import Post
from blog.services.admin_post_list_service import (
    get_admin_post_list_filters,
    get_admin_post_list_categories,
    get_admin_pinned_posts,
    get_admin_post_list_queryset,
)
from blog.services.pin_service import (
    AlreadyPinnedError,
    InvalidPinOrderError,
    NotPinnedError,
    PinLimitExceededError,
    add_pin,
    remove_pin,
    reorder_pins,
)
from blog.services.post_create_service import create_post
from blog.services.post_delete_service import delete_post
from blog.services.post_content_sanitize_service import sanitize_post_content

MAX_PIN_COUNT = 12
POSTS_PER_PAGE = 10
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


def _redirect_to_admin_post_list(request):
    referer = request.META.get("HTTP_REFERER")
    if referer and url_has_allowed_host_and_scheme(
        url=referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(referer)
    return redirect("blog:admin-post-list")


# 관리자 게시물 목록 조회
@admin_access_required
def admin_post_list_view(request):
    filters = get_admin_post_list_filters(request.GET)
    posts = get_admin_post_list_queryset(filters)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": get_admin_post_list_categories(),
        "pinned_posts": get_admin_pinned_posts(),
        "search": filters["search"],
        "category_id": filters["category_id"],
        "is_pinned": filters["is_pinned"],
        "ordering": filters["ordering"],
    }

    return render(request, "blog/admin/post_list.html", context)


# 관리자 게시물 생성
@admin_access_required
def admin_post_create_view(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            post = create_post(
                validated_data=form.cleaned_data,
                author=request.user,
            )
            return redirect(
                "blog:admin-post-detail",
                post_id=post.id,
            )

    else:
        form = PostCreateForm()

    return render(
        request,
        "blog/admin/post_create.html",
        {"form": form},
    )


# 관리자 게시물 상세보기
@admin_access_required
def admin_post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sanitized_content = sanitize_post_content(post.content)
    query_string = request.GET.urlencode()

    return render(
        request,
        "blog/admin/post_detail.html",
        {
            "post": post,
            "sanitized_content": sanitized_content,
            "query_string": query_string,
        },
    )


@staff_member_required
def admin_post_delete_view(request, post_id):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST 요청만 허용됩니다.")

    post = get_object_or_404(Post, id=post_id)
    delete_post(post)
    return redirect("blog:admin-post-list")


# pin 추가
@admin_access_required
@require_POST
def admin_pin_add_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    try:
        add_pin(post=post, max_count=MAX_PIN_COUNT)

    except AlreadyPinnedError:
        if _is_ajax_request(request):
            return JsonResponse({"message": "이미 고정된 게시물입니다."}, status=400)
        messages.warning(request, "이미 고정된 게시물입니다.")
        return _redirect_to_admin_post_list(request)

    except PinLimitExceededError:
        if _is_ajax_request(request):
            return JsonResponse(
                {"message": f"고정 게시물은 최대 {MAX_PIN_COUNT}개까지 가능합니다."},
                status=400,
            )
        messages.error(request, f"고정 게시물은 최대 {MAX_PIN_COUNT}개까지 가능합니다.")
        return _redirect_to_admin_post_list(request)

    except Exception:
        logger.exception("Failed to add pin for post_id=%s", post_id)
        if _is_ajax_request(request):
            return JsonResponse(
                {"message": "게시물 고정 중 오류가 발생했습니다."}, status=500
            )
        messages.error(request, "게시물 고정 중 오류가 발생했습니다.")
        return _redirect_to_admin_post_list(request)

    if _is_ajax_request(request):
        return JsonResponse({"message": "고정되었습니다."})

    messages.success(request, "게시물을 고정했습니다.")
    return _redirect_to_admin_post_list(request)


# pin 해제
@admin_access_required
@require_POST
def admin_pin_remove_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    try:
        remove_pin(post=post)

    except NotPinnedError:
        if _is_ajax_request(request):
            return JsonResponse({"message": "고정된 게시물이 아닙니다."}, status=400)
        messages.warning(request, "고정된 게시물이 아닙니다.")
        return _redirect_to_admin_post_list(request)

    except Exception:
        logger.exception("Failed to remove pin for post_id=%s", post_id)
        if _is_ajax_request(request):
            return JsonResponse(
                {"message": "고정 해제 중 오류가 발생했습니다."}, status=500
            )
        messages.error(request, "고정 해제 중 오류가 발생했습니다.")
        return _redirect_to_admin_post_list(request)

    if _is_ajax_request(request):
        return JsonResponse({"message": "고정이 해제되었습니다."})

    messages.success(request, "고정을 해제했습니다.")
    return _redirect_to_admin_post_list(request)


# pin 순서 변경
@admin_access_required
@require_POST
def admin_pin_reorder_view(request):
    raw_post_ids = request.POST.getlist("post_ids")

    try:
        post_ids = [int(post_id) for post_id in raw_post_ids]
        reorder_pins(post_ids=post_ids)

    except (ValueError, InvalidPinOrderError):
        return JsonResponse({"message": "잘못된 고정 순서 요청입니다."}, status=400)

    except Exception:
        logger.exception("Failed to reorder pins: post_ids=%s", raw_post_ids)
        return JsonResponse(
            {"message": "고정 순서 저장 중 오류가 발생했습니다."}, status=500
        )

    return JsonResponse({"message": "고정 순서가 저장되었습니다."})
