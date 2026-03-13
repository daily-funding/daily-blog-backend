from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseBadRequest

from blog.models import PostImage


@staff_member_required
def admin_image_upload_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST 요청만 허용됩니다.")

    uploaded_file = request.FILES.get("upload")
    if not uploaded_file:
        return HttpResponseBadRequest("업로드된 파일이 없습니다.")

    # 업로드 직후 PostImage 생성
    post_image = PostImage.objects.create(
        post=None,
        path=uploaded_file,
        capacity=uploaded_file.size,
    )

    image_url = post_image.path.url
    ck_func_num = request.GET.get("CKEditorFuncNum", "")

    # CKEditor4 업로드 응답 형식
    return HttpResponse(
        f"", # 추후 작성
        content_type="text/html",
    )
