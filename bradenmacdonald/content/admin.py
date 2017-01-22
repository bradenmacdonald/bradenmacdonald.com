from django.contrib import admin
from .models import BasicPage, ProjectGroup, Project

class BasicPageAdmin(admin.ModelAdmin):
    list_display = ('path', 'title', )

admin.site.register(BasicPage, BasicPageAdmin)

class ProjectGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', )

admin.site.register(ProjectGroup, ProjectGroupAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'year_range_str',)

admin.site.register(Project, ProjectAdmin)
