from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return self.name

class Author(models.Model):
    salutation = models.CharField(max_length=10) 
    full_name = models.TextField()
    birth_year = models.SmallIntegerField()  
    country = models.CharField(max_length=2)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')

    def __str__(self):
        return self.full_name


class Book(models.Model):  
    ISBN = models.CharField(max_length=13)  
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author,through='Inspiration',through_fields=('book', 'author'),)
    author = models.ForeignKey('Author', on_delete=models.CASCADE,related_name="author",)
    description = models.TextField()  
    year_release = models.SmallIntegerField()
    photo = models.ImageField(upload_to='book_images', blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    copy_count = models.SmallIntegerField(default = 1)
    redaction = models.ForeignKey('Redaction', on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    publication_date = models.DateField(auto_now = False ,null=True, auto_now_add = False)

    def __str__(self):
        return self.title


class Inspiration(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    inspirer = models.ForeignKey(Author,on_delete=models.CASCADE,related_name="inspired_works",)

class Redaction(models.Model):
    name = models.CharField(max_length=128)
    creation_year = models.SmallIntegerField()
    description = models.TextField()
 

    def __str__(self):
        return self.name


class Friend(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name




