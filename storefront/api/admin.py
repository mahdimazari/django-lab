from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Note, Category

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email']


# class ProfileAdmin(admin.ModelAdmin):
#     list_editable = ['verified']
#     list_display = ['user', 'full_name' ,'verified']

class NoteAdmin(admin.ModelAdmin):
    list_display=['author', "title", "content",  "created_at", "display_categories"]

    def display_categories(self, obj):
        # Get a comma-separated string of category names for the tags
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'categories'

class CategoryAdmin(admin.ModelAdmin):
    list_display=[ "name", "created_at"]    




# class TodoAdmin(admin.ModelAdmin):
#     list_editable = ['completed']
#     list_display = ['user', 'title' ,'completed', 'date']

# admin.site.register(User, UserAdmin)
# admin.site.register( Profile,ProfileAdmin)
admin.site.register( Note,NoteAdmin)
admin.site.register(Category, CategoryAdmin)

# admin.site.register( Todo,TodoAdmin)