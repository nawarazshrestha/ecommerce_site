from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "price",
            "discount_price",
            "content",
            "image",
            "draft",
            "publish"
        ]
