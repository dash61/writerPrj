from django.contrib.auth.decorators import login_required  # use for fn based views
from django.contrib.auth.mixins import LoginRequiredMixin  # use for class based views
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from .models import WriterPrjAllBooks
from .forms import WriterPrjAllBooksCreateForm, RegisterForm, ContactForm


# from https://kirr.co/bhpno4,   src->accounts->views.py, except he is modifying that code to do class based views
# This is for user registration.
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/' # go to home page; will need 1st to send an email for user to verify registration

    # override method to see if user is already registered, and if so, tell him
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)

# from https://github.com/codingforentrepreneurs/Django-User-Model-Unleashed/blob/master/src/accounts/views.py,
# at the end. We need a view for when the user clicks the link in his email.
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("/login")
    # invalid code
    return redirect("/login")


class HomeView(TemplateView):
    template_name = 'home.html'

    # override method of TemplateView to do special stuff:
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


"""
From: https://github.com/abidibo/aidsbank/blob/master/views.py, and modified.
This was his AssetUpdateManagerView function.
Contact Manager.
"""
class ContactManagerView(View):
    model = WriterPrjAllBooks
    slug_field = 'slug'
    form_class = ContactForm  # see forms.py for definition
    template_name = 'snippets/contact_manager.html'
    title = 'Contact Us'
    title_align_center = True

    def get(self, request, *args, **kwargs):  # default arg list
        context = {
            "form": self.form_class,
            "title": self.title,
            "title_align_center": self.title_align_center,
        }
        return render(request, "snippets/contact_manager.html", context)

    # This gets called when the form is successfully posted (ie, has no errors and Submit
    # is pressed). We don't need to do anything here but render the success html file.
    def post(self, request, *args, **kwargs):  # default arg list
        form_email = request.POST.get('email', '')
        form_message = request.POST.get('message', '')
        form_full_name = request.POST.get('full_name', '')

        # NOW YOU CAN DO THE WORK TO EMAIL THE ACTUAL DATA:
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'youotheremail@email.com']
        contact_message = "%s: %s via %s"%( 
                form_full_name, 
                form_message, 
                form_email)
        some_html_message = """
        <h1>hello</h1>
        """
        # DON'T REALLY SEND EMAIL YET, UNTIL YOU FILL IN REAL
        # EMAIL SETTINGS IN BASE.PY AND above.
        # send_mail(subject, 
        #         contact_message, 
        #         from_email, 
        #         to_email, 
        #         html_message=some_html_message,
        #         fail_silently=True)

        return render(request, "snippets/contact_manager_success.html", {})

class CreditsView(TemplateView):
    template_name = 'credits.html'

class LicenseView(TemplateView):
    template_name = 'license.html'

class BioView(TemplateView):
    template_name = 'bio.html'

@login_required()
def book_createview(request):
    form = WriterPrjAllBooksCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit=False) # not saved yet, but we do have an instance
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect("/books/")
        else:
            return HttpResponseRedirect('/login/')  # will deal with this later
    if form.errors:
        errors = form.errors

    template_name = 'writerhome/form.html'  # this file doesn't exist yet!
    context = {"form": form, "errors": errors}
    return render(request, template_name, context)


class BooksListView(ListView):
    template_name = 'writerhome/booksList.html' # could use default template name of <modelname_list.html>

    def get_queryset(self):
        return WriterPrjAllBooks.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(BooksListView, self).get_context_data(*args, **kwargs)
        qs = WriterPrjAllBooks.objects.all()
        if qs.exists():
            context['books'] = qs
        return context

# NOTE - THIS SHOULDN'T BE LOGIN REQUIRED, BUT ADMIN REQUIRED
class BookCreateView(LoginRequiredMixin, CreateView):
    form_class = WriterPrjAllBooksCreateForm
    template_name = 'form.html' # points now to more generic file in topmost templates folder
    success_url = '/books/'     # one way to do this; another is to define get_absolute_url on the model

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(BookCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(BookCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add A Book'
        return context

# NOTE - THIS SHOULDN'T BE LOGIN REQUIRED, BUT ADMIN REQUIRED
class BookUpdateView(LoginRequiredMixin, UpdateView):
    form_class = WriterPrjAllBooksCreateForm
    template_name = 'writerhome/detail-update.html' # new to be able to view detail and update at the same time
    login_url = '/login/'  # add this for the login mixin - MOVED TO BASE.PY SETTINGS FILE

    def get_context_data(self, *args, **kwargs):
        context = super(BookUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Book'
        return context

    def get_queryset(self):
        return WriterPrjAllBooks.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            print ("user cancelled the action!!!!!!")
            return HttpResponseRedirect(reverse_lazy('writerhome:list'))
        else:
            super(BookUpdateView, self).post(request, *args, **kwargs)
            return HttpResponseRedirect(reverse_lazy('writerhome:list'))

# TODO - PUT UP DIALOG AFTER SUCCESSFUL SAVE, WAIT 1.5 SECONDS, THEN REDIRECT TO LIST PAGE AGAIN
# COULD ALSO DO THIS IN SIGNALS.PY, DEFINE A POST SAVE SIGNAL HANDLER.

