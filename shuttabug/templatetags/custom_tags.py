from django import template
from shuttabug.forms import DownloadImageForm
from shuttabug.models import Photo
import os
from django.http import FileResponse
from django.http import HttpResponseRedirect

register = template.Library()
@register.inclusion_tag('shuttabug/download_image.html',takes_context=True)
def downloadform(context , **kwargs):
    photo_slug = kwargs['photo_slug'] #
    request = context.get('request',None)
    if request.method == "POST":
        form = DownloadImageForm(request.POST)
        if form.is_valid():
            pass
        else:
            print (form.errors)
    else:
        form = DownloadImageForm()

    context = {'form': form, 'photo_slug': photo_slug} #
    # context passed by downloadform tag used to render the form inside the front end tag?
    # context is also passed along to the request made by clicking buttons inside the template.
    return context