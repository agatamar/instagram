from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment,INSTAGRAM_MAXIMUM_COMMENT_LENGTH


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddCommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols': 80}),
        max_length=INSTAGRAM_MAXIMUM_COMMENT_LENGTH,
        label='')

    class Meta:
        model = Comment
        fields = ['content']
        labels = False