from django.conf.urls import url
from django.contrib import admin
#possibly redundant. takes visitor to /shuttabug/admin, but work eventually routes to photologue/admin/
# but without this step. default admin doesn't have taggit.!?
from . import views
from . views import myGalleryListView
from . views import PhotoDetailView
from . views import PhotoListView
from . views import DownLoadView
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^admin/$', admin.site.urls, name ='admin'),
    url(r'^gallerylist/$', myGalleryListView.as_view(), name ='custom-gallery-list'),
    url(r'^news/$',views.news, name ='news'),
    url(r'^search/$',views.search, name ='search'),
    url(r'^upload/$',views.upload_file, name ='upload'),

    url(r'^download_image/$',
        DownLoadView.as_view(),
        name='download_image'),

    url(r'^photo/(?P<photo_slug>[\w\-]+)/$',
        PhotoDetailView.as_view(),
        name='photo-detail'),
    url(r'^photolist/',
        PhotoListView.as_view(),
        name='photo-list'),

    ]
"""
    url(r'^download_image/(?P<photo_slug>[\w\-]+)/$',
        DownLoadImageView.as_view(),
        name='download_image'),
"""