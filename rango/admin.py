'''管理页面模块'''
from django.contrib import admin
from rango.models import Category, Page, UserProfile

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['category']}),
        ('Page Infomation', {'fields':['title', 'url', 'views']})
    ]

    list_display = ['title', 'category', 'url']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'views', 'likes']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
