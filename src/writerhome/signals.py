# Capitalization of 1st letters of each word of title is from string.capwords.
# Not the best solution, if you want to lowercase some words, like 'for' or 'and' or whatever, or even
# if you want a lowercase title entirely.

from django.db.models.signals import pre_save, post_save
from django.http import HttpResponseRedirect
from .utils import unique_slug_generator
#from .models import WriterPrjAllBooks
import string

# define callbacks
def wh_pre_save_receiver(sender, instance, dispatch_uid="wh_pre_save_receiver", *args, **kwargs):
    # for k, v in kwargs.items():
    #     print (k, v)
    # for count, thing in enumerate(args):
    #     print ('{0} - {1}'.format(count, thing))
    instance.title = string.capwords(instance.title) # force capitalization of first letters
    #print('saving... ' + instance.title)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    return HttpResponseRedirect('/list/')

# Note that post save is not too useful; could comment this out
# def wh_post_save_receiver(sender, instance, created, dispatch_uid="wh_post_save_receiver", *args, **kwargs):
#     print('saved...')
#     print(instance.title)

def signal_init():
    # wire callbacks to built-in django signals (pre_save and post_save)
    pre_save.connect(wh_pre_save_receiver, sender='writerhome.WriterPrjAllBooks')
    # post_save.connect(wh_post_save_receiver, sender='writerhome.WriterPrjAllBooks')


