from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from blog.models import PostImage


@csrf_exempt
@staff_member_required
def admin_image_upload_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST 요청만 허용됩니다.")

    uploaded_file = request.FILES.get("upload")
    if not uploaded_file:
        return JsonResponse(
            {
                "uploaded": 0,
                "error": {"message": "업로드된 파일이 없습니다."},
            },
            status=400,
        )

    post_image = PostImage.objects.create(
        post=None,
        path=uploaded_file,
        capacity=uploaded_file.size,
    )

    return JsonResponse(
        {
            "uploaded": 1,
            "fileName": uploaded_file.name,
            "url": post_image.path.url,
        }
    )
