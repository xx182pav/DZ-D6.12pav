"""my_site URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from common.views import index, RegisterView, CreateUserProfile  
from django.contrib.auth.views import LoginView, LogoutView  
from django.urls import reverse_lazy  
from django.urls import path, re_path, include 
from p_library import views
from p_library.views import index
from django.contrib.auth.views import LoginView, LogoutView
from p_library.views import AuthorEdit, AuthorList, author_create_many, books_authors_create_many
from p_library.views import PublisherDetailView, PublisherList
from django.conf.urls.static import static
from django.conf import settings


app_name = 'p_library'

urlpatterns = [
    path('', views.index),
    path('index/',views.index),
    path('', include('common.urls', namespace='common')),
    path('accounts/', include('allauth.urls')),  
    path('admin/', admin.site.urls),
    path('index/book_increment/', views.book_increment),
    path('index/book_decrement/', views.book_decrement),
    path('redactions', views.redactions),
    path('friends/', views.friends),
    path('create/', AuthorEdit.as_view(), name='author_create'),  
    path('authors', AuthorList.as_view(), name='author_list'),
    path('create_many/', author_create_many, name='author_create_many'),
    path('book_create_many/',books_authors_create_many, name='books_authors_create_many'),
    path("publishers", PublisherList.as_view()),

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
