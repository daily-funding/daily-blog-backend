import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import PostImage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "post 연결이 끊긴 24시간 지난 본문 이미지를 S3와 DB에서 삭제합니다."

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=24)

        # post_id=null이고, updated_at이 24시간이 지난 이미지를 targets으로 함
        targets = PostImage.objects.filter(
            post__isnull=True,
            updated_at__lte=cutoff,
        )

        deleted_count = 0
        failed_count = 0

        # 데이터의 양이 너무 많아질 경우에 대비하여 chunk_size씩 수행
        for post_image in targets.iterator(chunk_size=100):
            try:
                if not post_image.path:
                    post_image.delete()
                    deleted_count += 1
                    continue

                file_name = post_image.path.name
                storage = post_image.path.storage

                if file_name:
                    storage.delete(file_name)

                post_image.delete()
                deleted_count += 1

            except Exception:
                failed_count += 1
                logger.exception(
                    "Orphan post image cleanup failed",
                    extra={
                        "post_image_id": post_image.id,
                    },
                )

        # 결과 메시지 출력
        self.stdout.write(
            self.style.SUCCESS(
                f"[cleanup] done - deleted={deleted_count}, failed={failed_count}"
            )
        )
