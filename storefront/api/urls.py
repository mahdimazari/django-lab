from django.urls import path
from .views import CanteenDetailView, CanteenListView, CreateCanteenView, CreateSurveyCanteenView, CreateSurveyView, CreateUserView, SubmitSurveyResponseView, SurveyCanteenListView, SurveyCanteensView, SurveyDetailView, SurveyListView, SurveysUserView, UserPermissionsView, SurveyResponseDetailView, UserSurveyResponsesView, get_users, create_user, NoteListCreate, NoteDelete, get_categories
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
    path('survey-responses/', UserSurveyResponsesView.as_view(), name='user-survey-responses'),
    path('survey-responses/<int:pk>/', SurveyResponseDetailView.as_view(), name='user-survey-response-detail'),
    path('surveys/create/', CreateSurveyView.as_view(), name='create-survey'),
    path("notes/delete/<int:pk>/", NoteDelete.as_view(), name="delete-note"),
    path("categories/", get_categories, name='categories-list'),
     # Canteen endpoints
    path('canteens/', CanteenListView.as_view(), name='canteen-list'),
    path('canteens/create/', CreateCanteenView.as_view(), name='canteen-create'),
    path('canteens/<int:canteen_id>/', CanteenDetailView.as_view(), name='canteen-detail'),
    path('surveys/accessible/', SurveysUserView.as_view(), name='accessible-surveys'),
    # SurveyCanteen endpoints
    path('survey-canteens/', SurveyCanteenListView.as_view(), name='survey-canteen-list'),
    path('survey-canteens/create/', CreateSurveyCanteenView.as_view(), name='survey-canteen-create'),
    path('surveys/<int:survey_id>/canteens/', SurveyCanteensView.as_view(), name='survey_canteens'),
]


