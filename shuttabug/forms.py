from photologue.models import Photo
from simple_search import search_form_factory, search_filter

#SearchForm = search_form_factory(PhotoExtended.objects.all(),['tagged_items','tags'])
SearchForm = search_form_factory(Photo.objects.all(),['title','caption','slug','id','extended__tags__name'])
#'extended__tags__name' turns on search by tags.

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()