from blog.models import Post


def create_post(form, user):
    """
    관리자 게시물 생성 서비스
    """

    post = form.save(commit=False) # author 설정 전 저장 막음
    post.author = user # 현재 유저를 author로 설정
    post.save()

    return post
