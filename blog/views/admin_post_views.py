from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from blog.forms import PostCreateForm
from blog.models import Post
from blog.services.post_create_service import create_post
from blog.services.post_content_sanitize_service import sanitize_post_content


# 관리자 게시물 목록 조회
@staff_member_required
def admin_post_list_view(request):
    return HttpResponse("관리자 게시물 목록 페이지")


# 관리자 게시물 생성
@staff_member_required
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
@staff_member_required
def admin_post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sanitized_content = sanitize_post_content(post.content)

    return render(
        request,
        "blog/admin/post_detail.html",
        {
            "post": post,
            "sanitized_content": sanitized_content,
        },
    )
