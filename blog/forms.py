from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Category
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "category"]
        widgets = {"category": forms.CheckboxSelectMultiple}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class PostFilterForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    # category = forms.ChoiceField(
    #     label="Radio Button", widget=forms.RadioSelect, queryset=Category.objects.all()
    # )
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
