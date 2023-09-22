from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, ApplicationForm
from django.core.paginator import Paginator, Page
from .models import Category, Book, PageLimiter
from django.shortcuts import render, get_object_or_404


# Create your views here.

def index(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    e_mail = PageLimiter.objects.filter()[0]
    user = request.user
    
    limiter = int(PageLimiter.objects.filter()[0].limit) if len (PageLimiter.objects.filter()) >0 else 10
    per_page =int(request.GET.get('per_page', limiter)) 

    paginator = Paginator(books, per_page) 
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return render(request, 'app/index.html', {'categories': categories, 'e_mail': e_mail, 'page': page,})

def search_books(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(authors__icontains=query)

    return render(request, 'app/search_books.html', {'books': books, 'query': query})

def product_view(request, isbn):
    product = get_object_or_404(Book, isbn=isbn)
    # product.objects.filter()[0].categories
    books = Book.objects.filter(categories=Book.objects.filter(isbn=isbn)[0].categories)
    return render(request, 'app/product_template.html', {'product': product, 'books': books})

def category_view(request, categories):
    books = Book.objects.filter(categories=categories)
    return render(request, 'app/category_template.html', {'books': books})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/') 
            else:
                form.add_error(None, 'Неверные учетные данные')  
    else:
        form = LoginForm()
    
    return render(request, 'app/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/') 
    else:
        form = RegistrationForm()
    
    return render(request, 'app/register.html', {'form': form})

def application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # 'admin:index'
    else:
        form = ApplicationForm()
    return render(request, 'app/application.html', {'form': form})


def _logout(request):
        logout(request)
        return redirect('/') 