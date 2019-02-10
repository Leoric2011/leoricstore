import os
from random import randint

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page

def populate():
    python_pages = [
        {"title": "Offical Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/"},
        {"title":"How to Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/"}
    ]

    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title":"Django Rocks",
         "url":"http://www.djangorocks.com/"},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/",
         'views': 1000},
    ]

    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
         "url":"http://flask.pocoo.org"}
    ]

    cats = {
        "Python":{"pages": python_pages, 'likes':64, 'views':128},
        "Django":{"pages": django_pages, 'likes':32, 'views':64},
        "Other Frameworks":{"pages": other_pages, 'likes':16, 'views':32}
    }

    for cat, cat_data in cats.items():
        new_cat = add_cat(cat, cat_data['likes'], cat_data['views'])
        for page in cat_data['pages']:
            try:
                views = page['views']
            except KeyError:
                views = randint(50, 500)
            add_page(new_cat, page['title'], page['url'], views=views)

    for cat in Category.objects.all():
        for page in Page.objects.filter(category=cat):
            print("-{0}-{1}".format(str(cat), str(page)))

def add_page(cat, title, url, views=0):
    '''在数据库中新建页面'''
    new_page = Page.objects.get_or_create(category=cat, title=title)[0]
    new_page.url = url
    new_page.views = views
    new_page.save()
    return new_page

def add_cat(name, likes, views):
    '''在数据库中新建目录'''
    new_cat = Category.objects.get_or_create(name=name)[0]
    new_cat.likes = likes
    new_cat.views = views
    new_cat.save()
    return new_cat

def update_cat():
    pass
    # result_cats = Category.objects.all()
    # for cat in result_cats:
    #     if cat.name == "Python":
    #         cat.likes = 64
    #         cat.views = 128
    #         cat.save()
    #         continue
    #     if cat.name == "Django":
    #         cat.likes = 32
    #         cat.views = 64
    #         cat.save()
    #         continue
    #     if cat.name == "Other Frameworks":
    #         cat.likes = 16
    #         cat.views = 32
    #         cat.save()

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
    # update_cat()
