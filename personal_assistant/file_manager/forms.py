from django import forms
from .models import UploadedFile


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'folder']

    file_to_delete = forms.ModelChoiceField(
        queryset=UploadedFile.objects.all(),
        empty_label="Select a file to delete",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].required = False
