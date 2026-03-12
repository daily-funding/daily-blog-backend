from blog.models import Post

<<<<<<< HEAD
# 관리자 게시물 생성 서비스
def create_post(*, validated_data, author):
    return Post.objects.create(
        author=author,
        **validated_data, # 추후 데이터타입 확정되면 변경
=======

def create_post(*, validated_data, author):
    """
    관리자 게시물 생성 서비스
    """
    return Post.objects.create(
        author=author,
        **validated_data,
>>>>>>> ae81f26 (refactor: service가 ModelForm 구현에 의존하지 않도록 수정)
    )
