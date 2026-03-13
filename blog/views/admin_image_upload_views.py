import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest

from blog.models import PostImage
from blog.services.image_upload_service import validate_uploaded_image

logger = logging.getLogger(__name__)


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

    try:
        validate_uploaded_image(uploaded_file)

        post_image = PostImage.objects.create(
            post=None,
            path=uploaded_file,
            capacity=uploaded_file.size,
        )

    except ValidationError as e:
        return JsonResponse(
            {
                "uploaded": 0,
                "error": {"messages": e.messages},
            },
            status=400,
        )

    except Exception:
        logger.exception(
            "PostImage upload failed",
            extra={
                "file_name": uploaded_file.name,
                "file_size": uploaded_file.size,
                "content_type": uploaded_file.content_type,
            },
        )
        return JsonResponse(
            {
                "uploaded": 0,
                "error": {"message": "이미지 업로드 중 오류가 발생했습니다."},
            },
            status=500,
        )

    return JsonResponse(
        {
            "uploaded": 1,
            "fileName": uploaded_file.name,
            "url": post_image.path.url,
        }
    )
