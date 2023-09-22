from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    pageCount = models.CharField(max_length=100)
    publication_date = models.DateField(blank=True, null=True)
    thumbnailUrl = models.ImageField(blank=True, upload_to="images/")
    shortDescription = models.TextField(blank=True, null=True)
    longDescription = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    categories = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Application(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    # index = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class PageLimiter(models.Model):
    limit = models.CharField(max_length=3, unique=True)
    e_mail = models.EmailField(unique=True)
    
    def __str__(self):
        return f'Кол-во книг на странице: {self.limit} | Личный e-mail: {self.e_mail}'
    


@receiver(pre_save, sender=PageLimiter)
def prevent_multiple_objects(sender, instance, **kwargs):
    if sender.objects.exists() and not instance.pk:
        raise ValidationError('Можно создать только один объект модели')