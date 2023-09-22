import  requests, os, sys
from PIL import Image
from io import BytesIO


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookshop.settings")
import django
django.setup()
from app.models import *
from django.core.files import File


class LoadBookData():
    def __init__(self) -> None:
        self.books_source = str(sys.argv[1]) if len(sys.argv) > 1 else 'https://gitlab.grokhotov.ru/hr/yii-test-vacancy/-/raw/master/books.json'
        self.get_data()
        pass

    def _request_source(self):
        return requests.get(self.books_source)

    def add_new_image(self, url, model_instance):
        from urllib.request import urlopen
        image_name = url.split('/')[-1]
        response = urlopen(url)
        image_file = File(response)
        model_instance.thumbnailUrl.save(image_name, image_file)
        model_instance.save()
        
    def add_new_books(self, item):
        #if 'publishedDate' in item: publicationdate = item['publishedDate']['$date'].split('T')[0]
        book, book_created = Book.objects.get_or_create(title=item['title'] if 'title' in item else '', isbn=item['isbn']if 'isbn' in item else '',
        pageCount=item['pageCount']  if 'pageCount' in item else '',
        shortDescription=item['shortDescription'] if 'shortDescription' in item else '',
        longDescription=item['longDescription'] if 'longDescription' in item else '',  status=item['status'] if 'status' in item else '',
        authors= ','.join(str(x) for x in item['authors'])  if 'authors' in item else '', categories= ','.join(str(x) for x in item['categories']) if len(item['categories'])>=1 and 'categories' in item else 'Новинки')
        
        return book, book_created

    def add_new_categories(self, item):
        if len(item['categories'])>1: 
            for cat_item in item['categories']:
                if cat_item != '': category, category_created = Category.objects.get_or_create(name = cat_item)
        elif len(item['categories']) == 1: category, category_created = Category.objects.get_or_create(name = ','.join(str(x) for x in item['categories']))
        else: category, category_created = Category.objects.get_or_create(name = 'Новинки')

        return  category, category_created

    def get_data(self):
        for item in self._request_source().json():
            book, book_created = self.add_new_books(item)
            if book_created:
                try:
                    if 'thumbnailUrl' in item: self.add_new_image(item['thumbnailUrl'], Book.objects.get(title=item['title'], isbn = item['isbn']))
                except Exception as e:
                    print(e)
                    try:
                        if 'thumbnailUrl' in item: self.add_new_image(item['thumbnailUrl'], Book.objects.get(title=item['title']))
                    except Exception as e:
                        print(e)
                        pass
                print(f'Книга "{book.title}" создана')
            category, category_created = self.add_new_categories(item)
            if category_created: print(f'Категория "{category.name}" создана')
    
   
if __name__ == '__main__':
    LoadBookData()
    

