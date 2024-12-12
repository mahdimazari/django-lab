from django.urls import path
from .views import CreateSurveyView, CreateUserView, SubmitSurveyResponseView, SurveyDetailView, SurveyListView, UserPermissionsView, get_users, create_user, NoteListCreate, NoteDelete, get_categories
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .forms import SurveyStepOneForm, SurveyStepTwoForm,

urlpatterns = [
    path('users/', get_users, name='get_users'),
    # path('users/create/', create_user, name='create_user'),
    path("user/register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("notes/", NoteListCreate.as_view(), name='note-list'),
    path('surveys/', SurveyListView.as_view(), name='survey-list'),
    path('user-permissions/', UserPermissionsView.as_view(), name='permissions-list'),
    path('surveys/<int:survey_id>/', SurveyDetailView.as_view(), name='survey-detail'),
    path('surveys/<int:survey_id>/responses/', SubmitSurveyResponseView.as_view(), name='submit-response'),
     path('surveys/create/', CreateSurveyView.as_view(), name='create-survey'),
    path("notes/delete/<int:pk>/", NoteDelete.as_view(), name="delete-note"),
    path("categories/", get_categories, name='categories-list'),
]


