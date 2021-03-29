from django import template
from posts.models import Post

register = template.Library()


@register.filter
def post_total(user):
    PostForm = Post.objects.filter(user=user)
    post_count = PostForm.count()

