from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model  = Video
        fields = ["title", "comment", "image", "movie", "category", "tag"]

class VideoEditForm(forms.ModelForm):
    class Meta:
        model  = Video
        fields = ["title", "comment", "dt",]
