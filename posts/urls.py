from django.urls import path
from .views import (
    post_home,
    post_create,
    post_detail,
    post_update,
    post_delete,
)
app_name = 'posts'
urlpatterns = [
    path('post/',post_home, name="home"),
    path('post/create/',post_create, name="create"),
    path('post/<slug>/',post_detail, name="detail"),
    path('post/<slug>/edit/',post_update, name="update"),
    path('post/<slug:slug>/delete/',post_delete),
]
