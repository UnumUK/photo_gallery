from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from photologue.views import GalleryListView
from photologue.models import Photo, Gallery # use extended Gallery model later.

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