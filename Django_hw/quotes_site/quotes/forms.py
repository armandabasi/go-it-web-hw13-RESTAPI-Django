from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, Textarea, ModelChoiceField, Select
from django.core.exceptions import ValidationError
from taggit.forms import TagField

from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100, min_length=5, required=True,
                         widget=TextInput(attrs={"class": "form-control"}))
    born_date = CharField(widget=TextInput(attrs={"class": "form-control"}))
    born_location = CharField(max_length=200, widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(min_length=10, required=True,
                            widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ("fullname", "born_date", "born_location", "description")


class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all().order_by("fullname"), widget=Select(attrs={'class': 'form-select'}))
    quote = CharField(widget=TextInput(attrs={"class": "form-control"}))
    tags = TagField(widget=TextInput(attrs={"class": "form-control"}))

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tags_list = []
        if tags:
            for tag in tags:
                tag = Tag.objects.get_or_create(name=tag.strip())
                tags_list.append(str(tag[0].id))
        return tags_list

    class Meta:
        model = Quote
        fields = ("author", "quote", "tags")
