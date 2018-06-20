from django import forms
from django.contrib.auth import get_user_model
from .models import WriterPrjAllBooks
from .validators import validate_price
from .utils import code_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

User = get_user_model()


class ContactForm(forms.Form):
    full_name = forms.CharField(label="Full Name", required=False, max_length=100)
    email = forms.EmailField(label="Email", required=True, max_length=100, min_length=4, widget=forms.EmailInput)
    message = forms.CharField(label="Message", required=True, widget=forms.Textarea, max_length=5000)

    # do the following just to add the autofocus attr to the full_name field
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs) # need to call this or the next line fails
        self.fields['full_name'].widget.attrs.update({'autofocus':'autofocus'})

# from https://kirr.co/bhpno4,   src->accounts->forms.py
# This is for user registration, video chapter 44.
class RegisterForm(forms.ModelForm):  # old: UserCreationForm
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    # this makes sure the email is not already used by another user.
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email. It's already registered.")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)    # old: UserCreationForm
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # create a new user hash for activating email.

        if commit:
            user.save()
            self.send_activation_email(user)
        return user

    # Fn that was on CFE's Profile model class.
    # This call should be at the user level, not book objects. So make it a function here just for now.
    def send_activation_email(self, user):  # could use celery to delay the email
        print("Activating email now") # don't really do it


class WriterPrjAllBooksCreateForm(forms.ModelForm):
    class Meta:
        model = WriterPrjAllBooks
        fields = [
            'title',
            'author',
            'subtitle',
            'category',
            'price',
            'datePub'
        ]

    # Can do validation stuff here also
    def clean_title(self): # just prefix "clean_" to field name; calls forms.is_valid() - this is custom validation
        title = self.cleaned_data.get("title")
        if title == "Hello":
            raise forms.ValidationError("Not a valid title")
        return title
