from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from .validators import validate_price

User = settings.AUTH_USER_MODEL

class WriterPrjAllBooksQuerySet(models.query.QuerySet):
    def search(self, query): # WriterPrjAllBooks.objects.all().search(query) or WriterPrjAllBooks.objects.filter(something).search()
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

    def search(self, query): # WriterPrjAllBooks.objects.search()
        return self.get_queryset().search(query)

# You need a profile class if users are going to register and/or login.
# Video - https://www.youtube.com/watch?v=yDv5FIAeyoY
# CFE's try django 1.11.
# See video chapters 44&45 (7:28:13, 7:46:53) for details on registering.
# User profile starts at either chapter 37 (5:35:42) or 38 (5:54:00).

class WriterPrjAllBooks(models.Model):
    owner       = models.ForeignKey(User) # added at 4:02:00; call owner so as not to confuse with User
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

    # Fn that was on CFE's Profile model class, might need here (need to save email also).
    # This call should be at the user level, not book objects. So put it somewhere else for now.
    # def send_activation_email(self):  # could use celery to delay the email; look up
    #     print("Activating email now")
    #     pass

    # Use this if you don't have a title field; it will work with the utils.py
    # function 'unique_slug_generator'. Otherwise, comment this out.
    # @property
    # def title(self):
    #     return self.name


# examples to use from codrops:
# css:
# 3dbookshowcase
# BookBlock (mary lou)
# Fullscreen grid portfolio

# use lghtmesh.png backgnd from css/css3rotatingwords/images dir.