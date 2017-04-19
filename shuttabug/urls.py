from django.conf.urls import url
from django.contrib import admin
#possibly redundant. takes visitor to /shuttabug/admin, but work eventually routes to photologue/admin/
# but without this step. default admin doesn't have taggit.!?
from . import views
from photologue.views import GalleryListView

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^admin/$', admin.site.urls, name ='admin'),
    url(r'^gallerylist/$',
        GalleryListView.as_view(paginate_by=5),
        name = 'shuttabug-gallery-list'),
    ]