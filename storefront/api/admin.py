from django.contrib import admin
from django.db.models import Q


# Register your models here.
from .models import Canteen, Note,  Category


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display=['author', "title", "content",  "created_at", "display_categories"]
    list_filter = ('created_at', 'author')
    search_fields = ['title', 'categories__name']

    def display_categories(self, obj):
        # Get a comma-separated string of category names for the tags
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'categories'

class CategoryAdmin(admin.ModelAdmin):
    list_display=[ "name", "created_at"]    


# @admin.register(Note)
# class NoteAdmin(admin.ModelAdmin):
#     list_display = ['title', 'content', 'created_at']

admin.site.register(Category, CategoryAdmin)



@admin.register(Canteen)
class CanteenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'city', 'postal_code', 'daily_meal_count')
    search_fields = ('name', 'region', 'city', 'postal_code')
    # filter_horizontal = ('admins',)  # For many-to-many relationship
    list_filter = ('region', 'city')  # Add filtering options
    def get_form(self, request, obj=None, **kwargs):
        """
        Retire le champ 'admins' du formulaire d'ajout.
        """
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Lors de l'ajout d'une nouvelle cantine
            form.base_fields.pop('admins', None)  # Retire le champ 'admins' du formulaire
        return form
    def get_queryset(self, request):
        """
        Filtre les cantines affichées pour n'afficher que celles associées à l'utilisateur.
        """
        qs = super().get_queryset(request)  # Récupère le queryset par défaut
        user = request.user  # Utilisateur actuellement connecté
        print('user', user, qs)
        if user.is_superuser:
            return qs  # Les superusers voient toutes les cantines

        # Filtrer les cantines où l'utilisateur est admin ou consommateur
        return qs.filter(Q(admins=user) | Q(consumers=user)).distinct()

    def save_model(self, request, obj, form, change):
        """
        Ajoute automatiquement l'utilisateur actuel comme admin lors de la création.
        """
        # Sauvegarde l'objet en base de données pour obtenir un ID
        super().save_model(request, obj, form, change)
        
        if not change:  # Si c'est une nouvelle création
            obj.admins.add(request.user) 
