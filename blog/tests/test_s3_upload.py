import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# s3 업로드 테스트 
@pytest.mark.django_db
def test_s3_upload():
    file = ContentFile(b"hello pytest s3")

    path = default_storage.save("test/test.txt", file)

    assert path.startswith("test/")
