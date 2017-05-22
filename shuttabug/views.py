from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from photologue.views import GalleryListView
from photologue.models import Photo, Gallery # use extended Gallery model later.

from .forms import SearchForm

from django.http import HttpResponseRedirect
from .forms import UploadFileForm

# Create your views here.
def index(request):
    context= {'stuff':"Hello World. You are looking are Shuttabug index."}
    return render(request,'shuttabug/index.html', context)

class myGalleryListView(GalleryListView):
    template_name ='shuttabug/my_gallery_list.html'
    queryset = Gallery.objects.on_site().is_public() #possible redundant if I inherited properly
    context = {'object_list': queryset}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self,request, *args, **kwargs):
        pass

def news(request):
    context= {'stuff':"Hello World. You are looking are Shuttabug index."}
    return render(request,'shuttabug/news.html', context)

def upload_file(request):
    context= {'stuff':"Hello World. You are looking are Shuttabug index."}
    return render(request,'shuttabug/upload.html', context)

def photo_detail(request):
    context= {'stuff':"Hello World. You are looking are Shuttabug index."}
    return render(request,'shuttabug/photo_detail.html', context)

from django.views.static import serve
import os
def download_image(request):
    """
    serving image files for download during development
    """
    my_data = 'Good job'
    response = HttpResponse(my_data, content_type='force-download')
    response['Content-Disposition'] = 'attachment; filename="Example_download.txt"'
    return response

from django.views.generic.detail import DetailView

class PhotoDetailView(DetailView):
    template_name ='shuttabug/photo_detail.html'

    def get(self, request, photo_slug):
        # put all this in a try, except block to serve up a 404 page to people searching by slugs
        queryset = Photo.objects.on_site().is_public().get(slug = photo_slug)
        context = {'object': queryset}
        return render(request, self.template_name, context)

    def post(self,request, *args, **kwargs):
        pass

from django.views.generic.list import ListView
class PhotoListView(ListView):
    template_name ='shuttabug/photo_list.html'
    queryset = Photo.objects.on_site().is_public() #possible redundant if I inherited properly
    context = {'object_list': queryset}
    paginate_by = 20

    def get(self, request):
        #reverse('myviewname', kwargs={'pk': value})
        return render(request, self.template_name, self.context)

    def post(self,request):
        pass


@csrf_exempt
def search(request):
    form = SearchForm(request.GET or {})
    if request.method == 'GET' and 'q' in request.GET:
        q=request.GET['q']
        if q:
            if form.is_valid():
                results=set(form.get_queryset())

                similarPhotos =[]
                for result in results:
                    similarPhotos.extend(result.extended.tags.similar_objects())
                similarPhotos = set(similarPhotos)

                # set() - make sure the results are unique.
                #if results = 0, userMessage = no results returned, please try again
                userMessage = "Search for %s returns %s result" % (q,len(results))
                #This should be all in html. rather than view
        else:
            similarPhotos = None
            results=Photo.objects.none()
            userMessage="You didn’t enter any search criteria. Please enter some term" # or choose a category."

    else:
        similarPhotos = None
        results=Photo.objects.none()
        userMessage = None
    context ={
        'form':form,
        'similarPhotos': similarPhotos,
        'results':results, # dedupe queries that return lots of the same results. Ideally solve it at query level.
        'userMessage':userMessage,
        }
    return render(request, 'shuttabug/search.html',context)
