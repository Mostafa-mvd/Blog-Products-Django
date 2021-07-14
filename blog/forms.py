from django import forms
from blog.models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "category", "image"]
        widgets = {
            "title": forms.TextInput(attrs={'size': '40'}),
            "body": forms.Textarea(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
