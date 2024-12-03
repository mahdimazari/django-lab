from django.urls import path
from .views import CreateUserView, get_users, create_user, NoteListCreate, NoteDelete, CategoryViewSet, get_categories
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/', get_users, name='get_users'),
    # path('users/create/', create_user, name='create_user'),
    path("user/register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("notes/", NoteListCreate.as_view(), name='note-list'),
    path("notes/delete/<int:pk>/", NoteDelete.as_view(), name="delete-note"),
    path("categories/", get_categories, name='categories-list'),
]