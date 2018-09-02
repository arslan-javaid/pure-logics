from django import forms
from .models import Rack, Book


class RackForm(forms.ModelForm):

    class Meta:
        model = Rack
        fields = ['name']


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_year']
