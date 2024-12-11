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
from .models import Note, Survey, Category, User, SurveyResponse, Choice, Question
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .serializer import NoteSerializer, UserSerializer, CategorySerializer, SurveySerializer, AnswerSerializer, ResponseSerializer


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

class SurveyDetailView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request, survey_id):
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise NotFound({"error": "Survey not found"})  # Return 404 if survey does not exist

        serializer = SurveySerializer(survey)
        return Response(serializer.data)

class SubmitSurveyResponseView(APIView):
    def post(self, request, survey_id):
        data = request.data
        response_serializer = ResponseSerializer(data={'survey': survey_id})
        if response_serializer.is_valid():
            response = response_serializer.save()
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
            return Response({'message': 'Survey response submitted successfully!'})
        return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateSurveyView(APIView):
    def post(self, request):
        """
        Create a new survey with questions and choices.
        """
        data = request.data
        # user = request.user

        # Validate survey data
        survey_serializer = SurveySerializer(data={
            "title": data.get("title"),
            "description": data.get("description"),
            # "created_by": user.id,
        })

        if survey_serializer.is_valid():
            # Save the survey
            survey = survey_serializer.save()

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
# Create your views here.
