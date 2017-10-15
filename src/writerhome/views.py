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
from .forms import BookCreateForm, WriterPrjAllBooksCreateForm, RegisterForm, ContactForm


# from https://kirr.co/bhpno4,   src->accounts->views.py, except he is modifying that code to do class based views
# This is for user registration, video chapter 44.
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
# He changes this around for the current project at around 7:56:00+
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

# OLD STYLE FUNCTION BASED VIEWS, 1ST PASS AT VIEWS.
# def home(request):
#     context = {"html_var": "hi there"}
#     return render(request, "home.html", context)

# def about(request):
#     context = {"html_var": "hi there"}
#     return render(request, "about.html", context)

# def contact(request):
#     context = {"html_var": "hi there"}
#     return render(request, "contact.html", context)

# old way of doing this; works, but could use less code via TemplateView.
# your mileage may vary - you may want to do this still for some reason.
# class ContactView(View):
#     def get(self, request, *args, **kwargs):  # default arg list
#         context = {}
#         return render(request, "contact.html", context)
#     # could also define put and post methods the same way

class HomeView(TemplateView):
    template_name = 'home.html'
    print("inside class HomeView")

    # override method of TemplateView to do special stuff:
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        #print (context)
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
    print ("inside ContactManagerView")

    def get(self, request, *args, **kwargs):  # default arg list
        print ("inside get function")
        context = {
            "form": self.form_class,
            "title": self.title,
            "title_align_center": self.title_align_center,
        }
        return render(request, "snippets/contact_manager.html", context)

    # This gets called when the form is successfully posted (ie, has no errors and Submit
    # is pressed). We don't need to do anything here but render the success html file.
    def post(self, request, *args, **kwargs):  # default arg list
        print ("inside post function")
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


class BioView(TemplateView):
    print("inside class BioView")
    template_name = 'bio.html'

class BlogView(TemplateView):
    print("inside class BlogView")
    template_name = 'blog.html'

@login_required() # login_url='/login/') #  - MOVED login_url TO BASE.PY SETTINGS FILE
def book_createview(request):
    # form = BookCreateForm(request.POST or None)   # BETTER WAY OF DOING THINGS, BUT NOT BEST WAY
    # errors = None
    # if form.is_valid():
    #     obj = WriterPrjAllBooks.objects.create(
    #             title = form.cleaned_data.get('title'),
    #             subtitle = form.cleaned_data.get('subtitle'),
    #             price = form.cleaned_data.get('price')
    #         )
    #     return HttpResponseRedirect("/books/")
    # if form.errors:
    #     errors = form.errors
           
    # template_name = 'writerhome/form.html'
    # context = {"form": form, "errors": errors}
    # return render(request, template_name, context)
    form = WriterPrjAllBooksCreateForm(request.POST or None) # BETTER WAY #2; SEE BookCreateView for BEST way (near bottom)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():  # added this during 'adding user to db' series, see 4:20:00
            instance = form.save(commit=False) # not saved yet, but we do have an instance
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect("/books/")
        # can customize here, similar to a pre-save thing, OR can really use the signals and do this during pre-save
#        form.save()
        # can customize here, similar to a post-save thing, ditto
#        return HttpResponseRedirect("/books/")
        else:
            return HttpResponseRedirect('/login/')  # will deal with this later
    if form.errors:
        errors = form.errors
           
    template_name = 'writerhome/form.html'  # this file doesn't exist yet!
    context = {"form": form, "errors": errors}
    return render(request, template_name, context)


class BooksListView(LoginRequiredMixin, ListView):
    template_name = 'writerhome/booksList.html' # could use default template name of <modelname_list.html>

    def get_queryset(self):
        return WriterPrjAllBooks.objects.filter(owner=self.request.user)
        # slug = self.kwargs.get("slug") # kwargs is a dict
        # if slug:
        #     queryset = WriterPrjAllBooks.objects.filter(
        #             Q(title__iexact=slug) |
        #             Q(title__icontains=slug)
        #         )
        # else:
        #     queryset = WriterPrjAllBooks.objects.all()
        # return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(BooksListView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        #print(user)
        query = self.request.GET.get('q')
        items_exist = WriterPrjAllBooks.objects.filter(owner=user).exists()
        qs = WriterPrjAllBooks.objects.filter(owner=user).search(query)
        if items_exist and qs.exists():
            context['books'] = qs
        return context

class BookDetailView(LoginRequiredMixin, DetailView):
    template_name = 'writerhome/writerprjallbooks_detail.html' # using default name

    def get_queryset(self):
        return WriterPrjAllBooks.objects.filter(owner=self.request.user)

    # don't need this anymore:
    # def get_context_data(self, *args, **kwargs):
    #     #print (self.kwargs)
    #     context = super(BooksDetailView, self).get_context_data(*args, **kwargs)
    #     #print (context)
    #     return context

    # don't need this anymore after we wired up slugs right (and all db items have a slug):
    # def get_object(self, *args, **kwargs):
    #     book_id = self.kwargs.get('book_id')
    #     obj = get_object_or_404 (WriterPrjAllBooks, id=book_id) # or pk=book_id
    #     return obj

# BEST way of doing forms
class BookCreateView(LoginRequiredMixin, CreateView): # use mixin for class based views
    form_class = WriterPrjAllBooksCreateForm
    template_name = 'form.html' # points now to more generic file in topmost templates folder
    #login_url = '/login/'    # add this for the login mixin - MOVED TO BASE.PY SETTINGS FILE
    success_url = '/books/'  # one way to do this; another is to define get_absolute_url on the model

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        #instance.save()  # should not be needed here, done in super
        return super(BookCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(BookCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add A Book'
        return context

# BEST way of doing forms
class BookUpdateView(LoginRequiredMixin, UpdateView): # use mixin for class based views
    form_class = WriterPrjAllBooksCreateForm
    template_name = 'writerhome/detail-update.html' # new to be able to view detail and update at the same time
    login_url = '/login/'    # add this for the login mixin - MOVED TO BASE.PY SETTINGS FILE
    #success_url = '/books/'  # one way to do this; another is to define get_absolute_url on the model

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

