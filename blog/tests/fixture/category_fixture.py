import uuid
from blog.models import Category


def create_category(name=None):
    if name is None:
        name = f"test-category-{uuid.uuid4().hex[:8]}"
    return Category.objects.create(name=name)
