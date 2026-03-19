from django.db.models import Case, IntegerField, Q, When

from blog.models import Category, Pin, Post

DEFAULT_ORDERING = "latest"
VALID_ORDERINGS = {"latest", "updated", "title", "pinned"}


def get_admin_post_list_filters(query_params):
    ordering = query_params.get("ordering", DEFAULT_ORDERING)
    if ordering not in VALID_ORDERINGS:
        ordering = DEFAULT_ORDERING

    return {
        "search": query_params.get("search", "").strip(),
        "category_id": query_params.get("category", "").strip(),
        "is_pinned": query_params.get("is_pinned", "").strip(),
        "ordering": ordering,
    }


def get_admin_post_list_queryset(filters):
    posts = Post.objects.select_related("category", "author", "pin").all()

    search = filters["search"]
    category_id = filters["category_id"]
    is_pinned = filters["is_pinned"]
    ordering = filters["ordering"]

    if search:
        posts = posts.filter(
            Q(title__icontains=search)
            | Q(subtitle__icontains=search)
            | Q(description__icontains=search)
        )

    if category_id:
        posts = posts.filter(category_id=category_id)

    if is_pinned == "true":
        posts = posts.filter(pin__isnull=False)
    elif is_pinned == "false":
        posts = posts.filter(pin__isnull=True)

    if ordering == "latest":
        posts = posts.order_by("-created_at")
    elif ordering == "updated":
        posts = posts.order_by("-updated_at")
    elif ordering == "title":
        posts = posts.order_by("title")
    elif ordering == "pinned":
        posts = posts.annotate(
            pinned_order_group=Case(
                When(pin__isnull=False, then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by("pinned_order_group", "pin__sort_order", "-created_at")
    return posts


def get_admin_post_list_categories():
    return Category.objects.order_by("created_at")


def get_admin_pinned_posts():
    return Pin.objects.select_related("post").order_by("sort_order")
