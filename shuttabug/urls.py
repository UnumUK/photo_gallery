from django.conf.urls import url
from django.contrib import admin
#possibly redundant. takes visitor to /shuttabug/admin, but work eventually routes to photologue/admin/
# but without this step. default admin doesn't have taggit.!?
from . import views
from . views import myGalleryListView
from . views import myGalleryDetailView
from . views import myPhotoDetailView
from . views import myPhotoListView

from . views import myGalleryDateDetailView
from . views import myGalleryDayArchiveView
from . views import myGalleryMonthArchiveView
from . views import myGalleryYearArchiveView
from . views import myGalleryArchiveIndexView

from . views import myPhotoDateDetailView
from . views import myPhotoDayArchiveView
from . views import myPhotoMonthArchiveView
from . views import myPhotoYearArchiveView
from . views import myPhotoArchiveIndexView

from . views import DownLoadView
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^admin/$', admin.site.urls, name ='admin'),
    url(r'^news/$',views.news, name ='news'),
    url(r'^search/$',views.search, name ='search'),
    url(r'^upload/$',views.upload_file, name ='upload'),

    url(r'^download_image/$',
        DownLoadView.as_view(),
        name='download_image'),

    url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
        myGalleryDateDetailView.as_view(month_format='%m'),
        name='custom-gallery-date-detail'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
        myGalleryDayArchiveView.as_view(month_format='%m'),
        name='custom-gallery-archive-day'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
        myGalleryMonthArchiveView.as_view(month_format='%m'),
        name='custom-gallery-archive-month'),
    url(r'^gallery/(?P<year>\d{4})/$',
        myGalleryYearArchiveView.as_view(),
        name='custom-gallery-archive-year'),
    url(r'^gallery/$',
        myGalleryArchiveIndexView.as_view(),
        name='custom-gallery-archive'),

    url(r'^gallery/(?P<gallery_slug>[\w\-]+)/',
        myGalleryDetailView.as_view(),
        name='custom-gallery-detail'),

    url(r'^gallerylist/$',
        myGalleryListView.as_view(),
        name ='custom-gallery-list'),

    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
        myPhotoDateDetailView.as_view(month_format='%m'),
        name='custom-date-photo-detail'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
        myPhotoDayArchiveView.as_view(month_format='%m'),
        name='custom-photo-archive-day'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
        myPhotoMonthArchiveView.as_view(month_format='%m'),
        name='custom-photo-archive-month'),
    url(r'^photo/(?P<year>\d{4})/$',
        myPhotoYearArchiveView.as_view(),
        name='custom-pl-photo-archive-year'),
    url(r'^photo/$',
        myPhotoArchiveIndexView.as_view(),
        name='custom-pl-photo-archive'),
    # order of url mapping matters. try longer, more specific ones first
    url(r'^photo/(?P<photo_slug>[\w\-]+)/$',
        myPhotoDetailView.as_view(),
        name='custom-photo-detail'),

    url(r'^photolist/',
        myPhotoListView.as_view(),
        name='custom-photo-list'),

    ]
"""
    url(r'^download_image/(?P<photo_slug>[\w\-]+)/$',
        DownLoadImageView.as_view(),
        name='download_image'),
"""