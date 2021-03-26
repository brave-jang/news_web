from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            "post_url",
            "content",
            "content_img",
            "comment",
            "country",
            "category",
        ]
        widgets = {
            "post_url": forms.URLInput(),
            "category": forms.CheckboxSelectMultiple(),
        }


class CreatePostsForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            "post_url",
            "content",
            "content_img",
            "comment",
            "country",
            "category",
        ]
        widgets = {
            "post_url": forms.URLInput(),
            "category": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "post_url": "링크",
            "content": "내용",
            "content_img": "이미지 첨부",
            "comment": "코멘트",
            "country": "국가",
            "category": "카테고리",
        }
        help_texts = {
            "content": "기사내용을 요약해주세요.",
        }

    def save(self, *args, **kwargs):
        post = super().save(commit=False)
        return post
