from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from .validators import validate_price

User = settings.AUTH_USER_MODEL

class WriterPrjAllBooksQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()  # strip out whitespace on front and back, if any
            return self.filter(
                Q(title__icontains=query)|
                Q(title__iexact=query)|
                Q(author__icontains=query)|
                Q(author__iexact=query)|
                Q(subtitle__icontains=query)|
                Q(subtitle__iexact=query)
                ).distinct() # this makes sure if we match the same item with more than 1 Q, we only show it once
        return self

class WriterPrjAllBooksManager(models.Manager):
    def get_queryset(self):
        return WriterPrjAllBooksQuerySet(self.model, using=self._db)  # using same db

    def search(self, query):
        return self.get_queryset().search(query)


class WriterPrjAllBooks(models.Model):
    owner       = models.ForeignKey(User) # name this 'owner' so as not to confuse with User
    title       = models.CharField(max_length=128, blank=False, null=False)
    author      = models.CharField(max_length=100, blank=False, null=False)
    subtitle    = models.CharField(max_length=255, blank=True)
    category    = models.CharField(max_length=40, blank=True)
    image       = models.ImageField(max_length=255, blank=True) # requires the Pillow library
    datePub     = models.DateField(null=True, blank=False)
    price       = models.DecimalField(decimal_places=2, max_digits=5, validators=[validate_price]) # can give a list of validators
    descr       = models.TextField(max_length=2048, blank=True)
    abstract    = models.TextField(max_length=5000, blank=True)
    slug        = models.SlugField(null=True, blank=True)
    activated   = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=120, blank=True, null=True)

    objects = WriterPrjAllBooksManager()  # adds to Model.objects.all()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('writerhome:detail', kwargs={'slug': self.slug})
