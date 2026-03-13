from django.contrib.auth import get_user_model
from django.core.files import File

from blog.models import Post, Category

User = get_user_model()


def create_post(
    category: Category,
    author: User,
    preview_image: File,
    title="test title",
    subtitle="subtitle",
    description="description",
    content="content",
):
    return Post.objects.create(
        category=category,
        author=author,
        title=title,
        subtitle=subtitle,
        description=description,
        content=content,
        preview_image=preview_image,
    )
