from django.contrib import admin

# Register your models here.
from .models import WriterPrjAllBooks

class WriterPrjAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subtitle', 'descr', 'datePub', 'price', 'category',)
    search_fields = ['title', 'author', 'descr', 'abstract']

admin.site.register(WriterPrjAllBooks, WriterPrjAdmin)