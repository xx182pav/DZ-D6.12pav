from django.contrib import admin
from p_library.models import Book, Author, Redaction, Friend,Publisher


app_name = 'p_library'



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    @staticmethod
    def author_full_name(obj):
        return obj.author.full_name

    list_display = ['title', 'author_full_name','photo']
    fields = ['ISBN', 'title', 'description', 'year_release', 'author', 'price', 'copy_count', 'redaction','photo']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
 
    list_display = ['full_name']
    fields = ['full_name','birth_year','country']

@admin.register(Redaction)
class RedactionAdmin(admin.ModelAdmin):
    pass

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name",]
    fields = ["name"]

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name"]








# Register your models here.