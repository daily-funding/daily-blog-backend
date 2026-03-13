from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Post


class PostCreateForm(forms.ModelForm):
    content = forms.CharField(
        label="본문",
        widget=CKEditorUploadingWidget(config_name="admin_post"),
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
            "title": "제목",
            "subtitle": "부제목",
            "description": "미리보기 설명",
            "preview_image": "썸네일 이미지",
        }
        widgets = {
            "category": forms.Select(),
            "title": forms.TextInput(attrs={"placeholder": "제목을 입력하세요"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "부제목을 입력하세요"}),
            "description": forms.TextInput(
                attrs={"placeholder": "미리보기 설명을 입력하세요"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("제목은 비워둘 수 없습니다.")
        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data["subtitle"].strip()
        if not subtitle:
            raise forms.ValidationError("부제목은 비워둘 수 없습니다.")
        return subtitle

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if not description:
            raise forms.ValidationError("미리보기 설명은 비워둘 수 없습니다.")
        return description

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if not content:
            raise forms.ValidationError("본문은 비워둘 수 없습니다.")
        return content
