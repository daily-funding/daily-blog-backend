from blog.models import Post

# 관리자 게시물 생성 서비스
def create_post(*, validated_data, author):
    return Post.objects.create(
        author=author,
        **validated_data, # 추후 데이터타입 확정되면 변경
    )
