from photologue.models import Photo
from simple_search import search_form_factory, search_filter

#SearchForm = search_form_factory(PhotoExtended.objects.all(),['tagged_items','tags'])
SearchForm = search_form_factory(Photo.objects.all(),['title','caption','slug','id','extended__tags__name'])
#'extended__tags__name' turns on search by tags.

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class DownloadImageForm(forms.Form):
    CHOICES = (('facebook','Facebook'), ('linkedin','LinkedIn'), ('twitter','Twitter'),)
    download_options = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        required=True,
        )
    photo_slug = forms.CharField(max_length=50)
    def clean_my_field(self):
        """
        validation only for multiple choice fields, not radio.
        """
        if len(self.cleaned_data['download_options']) > 3:
            raise forms.ValidationError('Select no more than 3.')
        return self.cleaned_data['download_options']