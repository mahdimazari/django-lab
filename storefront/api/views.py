from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .filter import NoteFilter
from django.shortcuts import get_object_or_404, redirect
from .models import Note,Category, User,  Canteen
from djf_surveys.models import Survey
# from djf_surveys.serializers import SurveySerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .serializer import CanteenSerializer, NoteSerializer, UserSerializer, CategorySerializer,CanteenSerializer, SurveySerializer

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
    

class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # user.user_permissions.clear()
        permissions = [
            perm for perm in user.get_all_permissions()
            if user.has_perm(perm)
        ]
        groups = user.groups.values_list('name', flat=True)  # Groupes de l'utilisateur
        return Response({
            "username": user.username,
            "permissions": list(permissions),
            "groups": list(groups),
        })    
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['categories__name', 'title', 'content']
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = NoteFilter

    def validate(self, data):
        
        if not data.get('title'):
            raise ValidationError("Title is required.")
        return data

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    

    def perform_create(self, serializer):
        # Ensure the categories are being passed correctly
        categories = self.request.data.getlist('categories')
      
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


class SurveyListView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated] 



class SurveyListByCanteen(APIView):
    """
    Récupérer les surveys associés à une cantine donnée.
    """
    def get(self, request, canteen_id):
        try:
            # Récupérer la cantine par son ID
            canteen = Canteen.objects.get(id=canteen_id)
            
            # Récupérer les surveys associés à cette cantine via la relation ManyToMany
            surveys = canteen.relatedSurveys.all()
            
            # Sérialiser les surveys
            serializer = SurveySerializer(surveys, many=True)
            
            # Retourner la réponse
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Canteen.DoesNotExist:
            return Response({"error": "Canteen not found."}, status=status.HTTP_404_NOT_FOUND)




class SurveysUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Filtrer les cantines où l'utilisateur est admin ou consommateur
        cantines = Canteen.objects.filter(Q(admins=user) | Q(consumers=user))

        # Filtrer les surveys liés à ces cantines via SurveyCanteen
        survey_ids = Survey.objects.filter(canteen__in=cantines).values_list('survey_id', flat=True)
        surveys = Survey.objects.filter(id__in=survey_ids)

        # Sérialiser les surveys
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data)
    
class CanteensUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Filtrer les cantines où l'utilisateur est admin ou consommateur
        cantines = Canteen.objects.filter(consumers=user)

        # Filtrer les surveys liés à ces cantines via SurveyCanteen
        # survey_ids = SurveyCanteen.objects.filter(canteen__in=cantines).values_list('survey_id', flat=True)
        # surveys = Survey.objects.filter(id__in=survey_ids)

        # Sérialiser les surveys
        serializer = CanteenSerializer(cantines, many=True)
        return Response(serializer.data)

class SurveyDetailView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request, survey_id):
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise NotFound({"error": "Survey not found"})  

        serializer = SurveySerializer(survey)
        return Response(serializer.data)


class CanteenListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CanteenSerializer
    # print('canteen')
    def get_queryset(self):
        """
        Retourne les cantines où l'utilisateur est admin ou consommateur.
        """
        user = self.request.user  # Récupération de l'utilisateur connecté
        return Canteen.objects.filter(Q(admins=user) | Q(consumers=user)).distinct()

class CreateCanteenView(generics.CreateAPIView):
    queryset = Canteen.objects.all()
    serializer_class = CanteenSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate the authenticated user as an admin of the cantine
        canteen = serializer.save()
        canteen.admins.add(self.request.user)
        return canteen

class CanteenDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, canteen_id):
        canteen = get_object_or_404(Canteen, id=canteen_id)
        serializer = CanteenSerializer(canteen)
        return Response(serializer.data)
   