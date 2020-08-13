# from django.contrib.auth.models import User
from django import forms
from video.models import Video


class UploadFileForm(forms.Form):
    url = forms.CharField(max_length=101, required=False)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    # class Meta:
    #     model = Video
    #     fields = ['title', 'raw']
    #
    # def validate_unique(self):
    #     return True
