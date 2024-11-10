from django.contrib import admin

# Register your models here.
from .models import Application, CustomUser, Category

admin.site.register(Application)
admin.site.register(CustomUser)
admin.site.register(Category)