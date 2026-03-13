from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from blog.forms import PostCreateForm
from blog.models import Post
from blog.services.post_create_service import create_post


# 관리자 게시물 목록 조회
@staff_member_required
def admin_post_list_view(request):
    return HttpResponse("관리자 게시물 목록 페이지")


# 관리자 게시물 생성
@staff_member_required
def admin_post_list_view(request):
    return HttpResponse("관리자 게시물 목록 페이지")


# 관리자 게시물 생성
@staff_member_required
def admin_post_create_view(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            create_post(
                validated_data=form.cleaned_data,
                author=request.user,
            )
            return redirect("blog:admin-post-list")
        # 이후 게시물 자세히 보기로 돌아가는 것으로 변경 예정
    else:  # else 말고 다른 상황에 대해서 처리 구체화 해야함
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

    # 자세한 내용은 추후 구현
    return render(
        request,
        "blog/admin/post_detail.html",
        {"post": post},
    )
