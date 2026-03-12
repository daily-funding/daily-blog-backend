from blog.models import Post


def create_post(*, validated_data, author):
    """
    관리자 게시물 생성 서비스
    """
    return Post.objects.create(
        author=author,
        **validated_data,
    )
