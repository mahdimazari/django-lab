from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework import status, generics, viewsets
from .models import User, Note, Category
from .serializer import NoteSerializer, UserSerializer, CategorySerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['categories__name']

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        # Ensure the categories are being passed correctly
        categories = self.request.data.getlist('categories')
        print('test', self.request.data, categories)
        note = serializer.save(author=self.request.user)
        if categories:
            note.categories.set(categories)


class NoteDelete(generics.DestroyAPIView):
        queryset = Note.objects.all()
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            user = self.request.user
            return Note.objects.filter(author=user)
        
      
        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


       # To get a list of categories
    # @action(detail=False, methods=['get'])
@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

# Create your views here.
