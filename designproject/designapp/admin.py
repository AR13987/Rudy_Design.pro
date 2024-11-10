from django.contrib import admin

# Register your models here.
from .models import Project, FloorPlan, DesignSuggestion, Application, CustomUser, Category

admin.site.register(Project)
admin.site.register(FloorPlan)
admin.site.register(DesignSuggestion)
admin.site.register(Application)
admin.site.register(CustomUser)
admin.site.register(Category)