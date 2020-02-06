from django.shortcuts import render
from django.views.generic import FormView      
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from p_library.models import Author, Book, Redaction, Friend, Publisher  
from p_library.forms import AuthorForm, BookForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy 
from django.contrib.auth.forms import AuthenticationForm   
from django.forms import formset_factory  
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.detail import DetailView 
import json
      
  
  
# def login(request):  
#     if request.method == 'POST':  
#         form = AuthenticationForm(request=request, data=request.POST)  
#         if form.is_valid():  
#             auth.login(request, form.get_user())  
#             return HttpResponseRedirect(reverse_lazy('p_library:ind'))  
#     else:  
#         context = {'form': AuthenticationForm()}  
#         return render(request, 'login.html', context)  
  
  
# def logout(request):  
#     auth.logout(request)  
#     return HttpResponseRedirect(reverse_lazy('p_library:ind'))

class PublisherList(ListView):
    model = Publisher

    def get(self):
        publishers_list = self.model.objects.all()
        return publishers_list

    def put(self, request):
        data = json.loads(request.body)
        publisher = self.model(**data)
        publisher.save()

class PublisherDetailView(DetailView):
    
    model = Publisher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

# def books_list(request):
#     return HttpResponse('/index/ - для просмотра библиотеки; /redactions/ - для просмотра издательств; /friends/ - для просмотра друзей; /admin/ - для входа в админ. панель')

def index(request):
    template = loader.get_template('index.html')
    books_count = Book.objects.all().count()
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books_count": books_count,
        "books": books
    }
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def home(request):
    return render(request, 'home.html', locals())

def redactions(request):
    template = loader.get_template('redactions.html')
    redactions = Redaction.objects.all()
    books = Book.objects.all()
    data = {
        "redactions": redactions,
        "books": books,
    }
    return HttpResponse(template.render(data, request))

def friends(request):
    template = loader.get_template('friends.html')
    friends = Friend.objects.all()
    books = Book.objects.all()
    friends_data = {
        "friends": friends,
        "books": books,
    }
    return HttpResponse(template.render(friends_data, request))

class AuthorEdit(CreateView):  
    model = Author  
    form_class = AuthorForm  
    success_url = reverse_lazy('p_library:author_list')  
    template_name = 'authors_edit.html'  
  
  
class AuthorList(ListView):  
    model = Author  
    template_name = 'authors_list.html'

def author_create_many(request):  
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():  #  Проверяем, валидны ли данные формы
            for author_form in author_formset:  
                author_form.save()  #  Сохраним каждую форму в формсете
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:  #  Если обработчик получил GET запрос, значит в ответ нужно просто "нарисовать" формы.
        author_formset = AuthorFormSet(prefix='authors')  #  Инициализируем формсет и ниже передаём его в контекст шаблона.
    return render(request, 'manage_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):  
    AuthorFormSet = formset_factory(AuthorForm, extra=2)  
    BookFormSet = formset_factory(BookForm, extra=2)  
    if request.method == 'POST':  
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')  
        if author_formset.is_valid() and book_formset.is_valid():  
            for author_form in author_formset:  
                author_form.save()  
            for book_form in book_formset:  
                book_form.save()  
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))  
    else:  
        author_formset = AuthorFormSet(prefix='authors')  
        book_formset = BookFormSet(prefix='books')  
    return render(
	    request,  
		'manage_books_authors.html',  
		{  
	        'author_formset': author_formset,  
			'book_formset': book_formset,  
		}  
	)



