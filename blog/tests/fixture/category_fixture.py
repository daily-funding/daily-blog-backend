from blog.models import Category


def create_category(name="test category"):
    return Category.objects.create(name=name)
