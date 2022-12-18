from django import forms
from .models import *
from django.core.exceptions import ValidationError


# class AddPostForm(forms.Form):
#     # now this class is form wich is not connected to women class so we will make another one
#     # we can use widget to add specail css clases in forms but still use for cicle in temlates
#     title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-input'}))
#     slug = forms.SlugField(label="Slug filed")
#     content = forms.CharField(widget=forms.Textarea(
#         attrs={'cols': 60, 'rows': 10}), label="Information")
#     # required = True/False means that field required to fill out or not
#     is_published = forms.BooleanField(required=False)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(),
#                                  empty_label="Categoty not chosen")


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Enter a Category"

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # clean method starts with clean_ and then field which we whant to validate
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Lenth is longer than 200 symbols')
        return title
