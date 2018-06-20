"""writerhome URL Configuration

Include just the urls here needed for the app, so it is more reusable.

"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from .views import (
    BooksListView, BookCreateView, BookUpdateView) # use ()s to put on multiple lines (if a lot)

urlpatterns = [
    url(r'^create/$', BookCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', BookUpdateView.as_view(), name='detail'), # changed from BookDetailView to BookUpdateView, using just one now
    url(r'$', BooksListView.as_view(), name='list'),  # put last
]
