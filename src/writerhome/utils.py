'''
From: https://github.com/codingforentrepreneurs/Try-Django-1.11/blob/841ed24dcc21bef9be86d74d4ec30b8fe42ab376/src/restaurants/utils.py
'''

import random
import string

from django.conf import settings
from django.utils.text import slugify

'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/

This is the same as the code_generator down below.
'''

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Pass in an object from a model.
def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title) # MODIFY THIS IF YOU DON'T HAVE A TITLE FIELD, OR USE PROPERTY IN MODELS.PY.

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

#
# This code is from: https://github.com/codingforentrepreneurs/Django-User-Model-Unleashed/blob/master/src/accounts/utils.py
# We should put this in a utils.py file in the profile app, but we don't have a profile app. When you do, move this code.
#
# You can see a blog about this at: https://codingforentrepreneurs.com/blog, search for 'random string gen', find article
# named "Random String Generator in Python", 2/3/17.
#
SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 35)


def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))