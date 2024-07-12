from django import forms

from .models import Note
from .utils import validate_yt_url


class SubmitURLForm(forms.Form):
    url = forms.URLField(label="Enter a URL")

    def clean_url(self):
        url = self.cleaned_data.get("url")
        if validate_yt_url(url):
            return url
        else:
            raise forms.ValidationError("Please enter a valid YouTube URL.")
