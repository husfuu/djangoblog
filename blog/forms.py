from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


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

    def clean_text(self):
        KATA_KOTOR_LIST = ["anjing", "goblok", "kampret", "asw", "jancok"]
        text = self.cleaned_data["text"]

        for kata_kotor in KATA_KOTOR_LIST:
            text = text.replace(kata_kotor, "***")

        return text
        # for kata_kotor in KATA_KOTOR_LIST:
        #     if re.search(kata_kotor, string)


# def clean_text(self):
#     if self.cleaned_data["text"] in self.KATA_KOTOR:
#         for kata_kotor in self.KATA_KOTOR:
#             # print(kata_kotor)
#             if kata_kotor in self.cleaned_data["text"]:
#                 self.cleaned_data["text"] = self.cleaned_data["text"].replace(
#                     kata_kotor, "***"
#                 )

#     return self.cleaned_data["text"]

# kata_kotor = self.cleaned_data["text"].find("asw")
# print(kata_kotor)
# if kata_kotor:

# for kata in self.cleaned_data['text']:
#     print(kata)
# self.add_error("text", "error kata kotor")

# if Post.objects.filter(
#     text__in=["anjing", "goblok", "kampret", "asw", "jancok"]
# ):


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

    def clean(self):
        if self.cleaned_data["start_date"] > self.cleaned_data["end_date"]:
            self.add_error("start_date", "start date must be less than end date")
            self.add_error("end_date", "start date must be less than end date")
            # raise ValidationError("start date must be less than end date")


class EditPostForm(forms.Form):
    # fields = ["title", "text", "category"]
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def clean_text(self):
        KATA_KOTOR_LIST = ["anjing", "goblok", "kampret", "asw", "jancok"]
        text = self.cleaned_data["text"]

        for kata_kotor in KATA_KOTOR_LIST:
            # just replace kata kotor with "***", no need create validation wheter kata kotor is in text or not
            text = text.replace(kata_kotor, "***")

        return text

    def save(self, post):
        post.title = self.cleaned_data["title"]
        post.text = self.cleaned_data["text"]
        post.category.set(self.cleaned_data["category"])
        post.save()
