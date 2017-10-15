"""writerhome URL Configuration

Include just the urls here needed for the app, so it is more reusable.

"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from .views import (
    BooksListView, BookDetailView, BookCreateView, BookUpdateView) # use ()s to put on multiple lines (if a lot)

urlpatterns = [
    url(r'^create/$', BookCreateView.as_view(), name='create'),
    #url(r'^(?P<slug>[\w-]+)/update/$', BookUpdateView.as_view(), name='update'), # put so it finds this first before the next one
    url(r'^(?P<slug>[\w-]+)/$', BookUpdateView.as_view(), name='detail'), # changed from BookDetailView to BookUpdateView, using just one now
    url(r'$', BooksListView.as_view(), name='list'),  # put last
]

    #url(r'^books/create/$', book_createview, name='create'), # old way
    
# This didn't help to see the images; putting this in the other urls.py file DID.
# if settings.DEBUG:
#     urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
#     urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
