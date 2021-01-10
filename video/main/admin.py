from django.contrib import admin
from .models import Category, Video

# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display =('id','title')

admin.site.register(Category,AdminCategory)
admin.site.register(Video)