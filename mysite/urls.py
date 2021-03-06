"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #overrides default photologue url match.
    #url(r'^$', include('shuttabug.urls',namespace='shuttabug')),
    #url(r'^photologue/', include('shuttabug.urls',namespace='shuttabug')),
    url(r'^photologue/',include('photologue.urls',namespace='photologue')),
    url(r'^shuttabug/', include('shuttabug.urls',namespace='shuttabug')),
] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
if settings.DEBUG:
    ### To test ###
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
