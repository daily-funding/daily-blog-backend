from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from blog.forms import PostCreateForm
from blog.services.post_create_service import create_post


@staff_member_required
def admin_post_create_view(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            create_post(form=form, user=request.user)
            return redirect("blog:admin-post-list")
    else:
        form = PostCreateForm()

    return render(
        request,
        "blog/admin/post_create.html",
        {"form": form},
    )
