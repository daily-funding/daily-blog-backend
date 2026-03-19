from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Category, Post


class PostCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by("created_at"),
        label="카테고리",
        widget=forms.Select(),
        empty_label="카테고리를 선택하세요",
        error_messages={"required": "카테고리는 비워둘 수 없습니다."},
    )
    title = forms.CharField(
        label="제목",
        widget=forms.Textarea(
            attrs={
                "placeholder": "제목을 입력하세요",
                "rows": 3,
                "maxlength": Post._meta.get_field("title").max_length,
                "aria-label": "제목",
            }
        ),
        error_messages={"required": "제목은 비워둘 수 없습니다."},
    )
    subtitle = forms.CharField(
        label="부제목",
        widget=forms.Textarea(
            attrs={
                "placeholder": "부제목을 입력하세요",
                "rows": 3,
                "maxlength": Post._meta.get_field("subtitle").max_length,
                "aria-label": "부제목",
            }
        ),
        error_messages={"required": "부제목은 비워둘 수 없습니다."},
    )
    description = forms.CharField(
        label="미리보기 설명",
        widget=forms.Textarea(
            attrs={
                "placeholder": "미리보기 설명을 입력하세요",
                "rows": 4,
                "maxlength": Post._meta.get_field("description").max_length,
                "aria-label": "미리보기 설명",
            }
        ),
        error_messages={"required": "미리보기 설명은 비워둘 수 없습니다."},
    )
    content = forms.CharField(
        label="본문",
        widget=CKEditorUploadingWidget(config_name="admin_post"),
        error_messages={"required": "본문은 비워둘 수 없습니다."},
    )

    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "subtitle",
            "description",
            "content",
            "preview_image",
        ]
        labels = {
            "category": "카테고리",
            "preview_image": "썸네일 이미지",
        }
        widgets = {
            "category": forms.Select(attrs={"aria-label": "카테고리"}),
            "preview_image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/png,image/jpeg,image/webp,image/jpg",
                    "aria-label": "썸네일 이미지",
                }
            ),
        }

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_subtitle(self):
        return self.cleaned_data["subtitle"].strip()

    def clean_description(self):
        return self.cleaned_data["description"].strip()

    def clean_content(self):
        return self.cleaned_data["content"].strip()
