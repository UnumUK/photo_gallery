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
    queryset = Gallery.objects.on_site().is_public #possible redundant if I inherited properly
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
