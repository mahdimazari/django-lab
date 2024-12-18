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
from .models import Note, Survey, Category, User, SurveyResponse, Choice, Question, Canteen, SurveyCanteen
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .serializer import NoteSerializer, UserSerializer, CategorySerializer, SurveySerializer, AnswerSerializer, SurveyResponseSerializer,CanteenSerializer, SurveyCanteenSerializer

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
        print("test")
        if not data.get('title'):
            raise ValidationError("Title is required.")
        return data

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


class SurveyListView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated] 



class SurveysUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Filtrer les cantines où l'utilisateur est admin ou consommateur
        cantines = Canteen.objects.filter(Q(admins=user) | Q(consumers=user))

        # Filtrer les surveys liés à ces cantines via SurveyCanteen
        survey_ids = SurveyCanteen.objects.filter(canteen__in=cantines).values_list('survey_id', flat=True)
        surveys = Survey.objects.filter(id__in=survey_ids)

        # Sérialiser les surveys
        serializer = SurveySerializer(surveys, many=True)
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

# class SubmitSurveyResponseView(APIView):
#     def post(self, request, survey_id):
#         data = request.data
#         response_serializer = SurveyResponseSerializer(data={'survey': survey_id})
#         if response_serializer.is_valid():
#             response = response_serializer.save()
#             for answer_data in data.get('answers', []):
#                 answer_serializer = AnswerSerializer(data={
#                     'response': response.id,
#                     'question': answer_data['question'],
#                     'text': answer_data.get('text', ''),
#                     'choice': answer_data.get('choice', None),
#                 })
#                 if answer_serializer.is_valid():
#                     answer_serializer.save()
#                 else:
#                     return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response({'message': 'Survey response submitted successfully!'})
#         return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubmitSurveyResponseView(APIView):
    """
    Vue pour soumettre une réponse à un survey, associée à une cantine donnée.
    """

    def post(self, request, survey_id):
        data = request.data
        print('data', data.get("canteen_id"))
        # Vérifier si la cantine est fournie
        canteen_id = data.get("canteen_id")
        user = request.user
        print('canteen', canteen_id, user)
        if not canteen_id:
            return Response({"error": "Canteen ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier que la cantine existe
        try:
            canteen = Canteen.objects.get(id=canteen_id)
            print('ok')
        except Canteen.DoesNotExist:
            return Response({"error": "Canteen not found."}, status=status.HTTP_404_NOT_FOUND)

        # Valider la réponse
        response_serializer = SurveyResponseSerializer(data={'survey': survey_id, 'cantine': canteen_id, 'created_by': user.id})
        if response_serializer.is_valid():
            # Sauvegarder la réponse
            response = response_serializer.save()
            print('response', response, response_serializer)

            # Associer la cantine à la réponse
            # response.cantine.add(canteen)
            # response.save()

            # Enregistrer les réponses aux questions
            for answer_data in data.get('answers', []):
                answer_serializer = AnswerSerializer(data={
                    'response': response.id,
                    'question': answer_data['question'],
                    'text': answer_data.get('text', ''),
                    'choice': answer_data.get('choice', None),
                })
                if answer_serializer.is_valid():
                    answer_serializer.save()
                else:
                    return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Survey response submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SurveyResponseDetailView(generics.RetrieveUpdateAPIView):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Récupère une instance spécifique de SurveyResponse pour l'utilisateur.
        """
        user = self.request.user
        response_id = self.kwargs.get("pk")  # Récupère l'ID de la réponse
        try:
            response = SurveyResponse.objects.get(id=response_id, created_by=user)
        except SurveyResponse.DoesNotExist:
            raise NotFound({"error": "Response not found or you do not have access"})
        return response

class UserSurveyResponsesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer toutes les réponses de l'utilisateur connecté
        user = request.user
        responses = SurveyResponse.objects.filter(created_by=user)

        # Sérialiser les réponses
        serializer = SurveyResponseSerializer(responses, many=True)
        return Response(serializer.data)
    
class CreateSurveyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Create a new survey with questions and choices.
        """
        data = request.data
        user = request.user
        print('user', user.id) 

        # Validate survey data
        survey_serializer = SurveySerializer(data={
            "title": data.get("title"),
            "description": data.get("description"),
        })

        if survey_serializer.is_valid():
            # Save the survey and associate it with the user
            survey = self.perform_create(survey_serializer, user)

            # Save each question
            for question_data in data.get("questions", []):
                question = Question.objects.create(
                    survey=survey,
                    text=question_data.get("text"),
                    question_type=question_data.get("question_type"),
                    required=question_data.get("required", True),
                )

                # Save choices for the question (if applicable)
                for choice_text in question_data.get("choices", []):
                    Choice.objects.create(question=question, text=choice_text)

            return Response(
                {"message": "Survey created successfully!", "survey_id": survey.id},
                status=status.HTTP_201_CREATED,
            )

        return Response(survey_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer, user):
        """
        Custom save method to associate the user with the survey.
        """
        # Add the user to the survey before saving
        survey = serializer.save(created_by=user)  # Associate the user
        return survey

    def get_queryset(self):
        user = self.request.user
        return Survey.objects.filter(created_by=user)

class CanteenListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CanteenSerializer
    print('canteen')
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
    
class SurveyCanteenListView(ListAPIView):
    serializer_class = SurveyCanteenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve all survey-canteen mappings for the authenticated user's cantines.
        """
        user_cantines = self.request.user.admin_cantines.all()  # Cantines managed by this user
        return SurveyCanteen.objects.filter(canteen__in=user_cantines)
    
class SurveyCanteensView(APIView):
    """
    Retourne toutes les cantines associées à un survey spécifique.
    """
    def get(self, request, survey_id):
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return Response({"error": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Récupérer les cantines associées à ce survey via la table intermédiaire SurveyCanteen
        survey_canteens = SurveyCanteen.objects.filter(survey=survey)
        canteens = [survey_canteen.canteen for survey_canteen in survey_canteens]
        
        # Sérialiser les cantines
        serializer = CanteenSerializer(canteens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateSurveyCanteenView(generics.CreateAPIView):
    serializer_class = SurveyCanteenSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Check if the user has permission to link the survey to the canteen.
        """
        canteen = serializer.validated_data['canteen']
        survey = serializer.validated_data['survey']

        # Ensure the user is an admin of the canteen
        if not canteen.admins.filter(id=self.request.user.id).exists():
            raise serializer.ValidationError("You do not have permission to link a survey to this canteen.")

        # Save the SurveyCanteen object
        return serializer.save()

# Create your views here.
