from django.shortcuts import render, render_to_response
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.http import HttpResponse
from django.http import FileResponse
from photologue.views import GalleryListView, GalleryDetailView,GalleryDateView,PhotoDateView
#from photologue.views import PhotoDateDetailView, PhotoDateDetailView, PhotoMonthArchiveView, PhotoYearArchiveView
from photologue.models import Photo, Gallery # use extended Gallery model later.
import os
from .forms import SearchForm, DownloadImageForm

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
    paginate_by = 20
    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass

class myGalleryDetailView(GalleryDetailView):
    template_name ='shuttabug/my_gallery_detail.html'

    def get(self,request, gallery_slug):
        queryset=Gallery.objects.on_site().is_public().get(slug = gallery_slug)
        context ={'gallery': queryset}
        return render(request, self.template_name, context)
    def post(self, request):
        pass

class myGalleryDateDetailView(GalleryDateView, DateDetailView):
    template_name = 'shuttabug/my_photo_archive.html'#???

class myGalleryArchiveIndexView(GalleryDateView, ArchiveIndexView):
    template_name = 'shuttabug/my_gallery_archive.html'


class myGalleryDayArchiveView(GalleryDateView, DayArchiveView):
    template_name = 'shuttabug/my_gallery_archive_day.html'


class myGalleryMonthArchiveView(GalleryDateView, MonthArchiveView):
    template_name = 'shuttabug/my_gallery_archive_month.html'


class myGalleryYearArchiveView(GalleryDateView, YearArchiveView):
    make_object_list = True
    template_name = 'shuttabug/my_gallery_archive_year.html'

def news(request):
    context= {'stuff':"Hello World. You are looking are Shuttabug index."}
    return render(request,'shuttabug/news.html', context)

def upload_file(request):
    context= {'stuff':"Hello World. You are looking are Shuttabug index."}
    return render(request,'shuttabug/upload.html', context)

from django.views.generic.detail import DetailView

class myPhotoDetailView(DetailView):
    template_name ='shuttabug/my_photo_detail.html'

    def get(self, request, photo_slug):
        # put all this in a try, except block to serve up a 404 page to people searching by slugs that do not exist
        queryset = Photo.objects.on_site().is_public().get(slug = photo_slug)
        context = {'object': queryset}
        return render(request, self.template_name, context)

    def post(self,request, *args, **kwargs):
        pass

class myPhotoListView(ListView):
    template_name ='shuttabug/my_photo_list.html'
    queryset = Photo.objects.on_site().is_public() #possible redundant if I inherited properly
    context = {'object_list': queryset}
    paginate_by = 20

    def get(self, request):
        return render(request, self.template_name, self.context)

class myPhotoArchiveIndexView(PhotoDateView, ArchiveIndexView):
    template_name='shuttabug/my_photo_archive.html'

class myPhotoDateDetailView(PhotoDateView,DateDetailView):
    # redundant, have used photodetailview in urls.
    template_name='shuttabug/my_photo_date_detail.html'

class myPhotoDayArchiveView(PhotoDateView, DayArchiveView):
    template_name='shuttabug/my_photo_archive_day.html'

class myPhotoMonthArchiveView(PhotoDateView, MonthArchiveView):
    template_name='shuttabug/my_photo_archive_month.html'

class myPhotoYearArchiveView(PhotoDateView, YearArchiveView):
    make_object_list = True
    template_name='shuttabug/my_photo_archive_year.html'



class DownLoadView(DetailView):
    template_name ='shuttabug/download_image.html'
    def get(self, request):
        form = DownloadImageForm()
        context ={'form':form}
        return render(request, self.template_name, context)

    def post(self,request):
        """ update User app usage statistics when User is implemented. """
        if request.method == "POST":
            form = DownloadImageForm(request.POST)
            if form.is_valid():
                selection = request.POST["download_options"]
                photo_slug = request.POST["photo_slug"]
                #can cut all this if just pass photo.image.file_path instead of photo.slug in photo details template
                photo= Photo.objects.on_site().is_public().get(slug = photo_slug )
                file_path = str(photo.image.file)
                #### if os.path.exists(file_path): #nice test ####
                file_name, file_extension = os.path.splitext(file_path)
                file_name = file_name.split('/')[-1]
                response = FileResponse(open(file_path,'rb'))
                response['content_type']='force-download'
                response['Content-Disposition'] = 'attachment; filename="%s_download%s"' % (file_name, file_extension)
                return response
            else:
                print (form.errors)
                form = DownloadImageForm()
                context = {'form':form}
                # if form is incomplete, need to render an error page rather than just download_image
        #### this and the GET method is redundant. you can't access 'shuttabug/download_image/' except by request.POST ###
        #### need to render an error page or redirect ####
        #### the download template doesn't depend on the view.py function to render. customtags ####
        return render(request, self.template_name, context)
import json
def jsonTesting(request):
    template_name = 'json_test.html'
    data ={}
    if request.method =='POST':
        data = json.loads(request.text)
        email = data['email']
        context ={'data':data}
        return render(request, template_name, context)
    else:
        context ={'data':data}
        return render(request, template_name, context)

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
