"""writerprj URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from writerhome.views import (
    HomeView, AboutView, RegisterView, activate_user_view,
    BioView, ContactManagerView,
    CreditsView, LicenseView)

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contact/$', ContactManagerView.as_view(), name='contact'),
    url(r'^bio/$', BioView.as_view(), name='bio'),
    url(r'^credits/$', CreditsView.as_view(), name='credits'),
    url(r'^license/$', LicenseView.as_view(), name='license'),
    url(r'^blog/', include('django_blog_it.urls')),
    url(r'^books/', include('writerhome.urls', namespace='writerhome')), # now url includes books
    url(r'^$', HomeView.as_view(), name='home'),
]
# This allows viewing the images on the booklist, using <img src={{ obj.image.url }}>.
if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
