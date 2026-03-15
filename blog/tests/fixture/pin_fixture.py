from blog.models import Post, Pin

def create_pin(
        post: Post,
        sort_order=1,
):
    return Pin.objects.create(
        post=post,
        sort_order=sort_order
    )
