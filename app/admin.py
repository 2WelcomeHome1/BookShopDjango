from django.contrib import admin
from .models import Book, Category, PageLimiter, Application

# Register your models here.

class Limiter(admin.ModelAdmin):
    list_per_page = 10  # Устанавливаем количество экземпляров на страницу


admin.site.register(Category, Limiter)
admin.site.register(Book, Limiter)
admin.site.register(PageLimiter)
admin.site.register(Application)



