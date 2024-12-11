from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Note, Category, Survey, Question, Answer, SurveyResponse, Choice

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email']


# class ProfileAdmin(admin.ModelAdmin):
#     list_editable = ['verified']
#     list_display = ['user', 'full_name' ,'verified']

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


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'created_at']

admin.site.register(Category, CategoryAdmin)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Allows adding extra empty rows for new questions
    fields = ['id', 'survey', 'text', 'question_type', 'required']  # Include survey and question IDs
    readonly_fields = ['id', 'survey']  # Make Survey ID visible and readonly in the detail page

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']  # Display ID in the survey list view
    inlines = [QuestionInline]
    readonly_fields = ['id']  # Make Survey ID visible and readonly in the detail page

class AnswerInline(admin.TabularInline):
    """
    Inline display of Answer records in SurveyResponse admin.
    """
    model = Answer
    extra = 0  # No extra blank forms by default
    fields = ('question', 'text', 'choice')  # Fields to display in the inline table
    readonly_fields = ('question',)  # Make the question field read-only
    show_change_link = True  # Allow navigating to the Answer detail page

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    """
    Admin configuration for SurveyResponse.
    """
    list_display = ('id', 'survey', 'created_at')  # Fields to display in the list view
    list_filter = ['survey', 'created_at']  # Filters for easy navigation
    # search_fields = ('user__username', 'survey__title')  # Searchable fields
    date_hierarchy = 'created_at'  # Date hierarchy navigation
    inlines = [AnswerInline]  # Display answers inline within the SurveyResponse admin

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for Answer.
    """
    list_display = ('id', 'get_survey',  'text')
    list_filter = ['question']  # Filters for easy navigation
    # search_fields = ('response__user__username', 'response__survey__title', 'text')  # Searchable fields
    # date_hierarchy = 'created_at'  # Date hierarchy navigation
    # autocomplete_fields = ('response', 'question', 'choice')  # Autocomplete for foreign keys

    def get_survey(self, obj):
        """Retrieve the survey related to this answer."""
        return obj.response.survey.title
    get_survey.short_description = 'Survey'  # Label for the column in the admin

    def get_user(self, obj):
        """Retrieve the user who submitted this answer."""
        return obj.response.user.username
    get_user.short_description = 'User'  # Label for the column in the admin