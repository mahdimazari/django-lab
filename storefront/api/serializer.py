from rest_framework import serializers
from .models import Note, User, Category, Survey, Question, Answer, SurveyResponse, Choice, Canteen, SurveyCanteen



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'required', 'choices']

class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'created_by', 'description', 'questions']
        extra_kwargs = {'created_by': {"read_only": True}}


class CanteenSerializer(serializers.ModelSerializer):
    admins = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    consumers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Canteen
        fields = ['id', 'name', 'region', 'city', 'postal_code', 'daily_meal_count', 'admins', 'consumers']

class SurveyCanteenSerializer(serializers.ModelSerializer):
    survey = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all())
    canteen = serializers.PrimaryKeyRelatedField(queryset=Canteen.objects.all())

    class Meta:
        model = SurveyCanteen
        fields = ['id', 'survey', 'canteen']
class AnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    choice_text = serializers.CharField(source='choice.text', read_only=True)
    class Meta:
        model = Answer
        fields = ['id', 'response', 'question', 'question_text', 'text', 'choice', 'choice_text']
class SurveyResponseSerializer(serializers.ModelSerializer):
    survey = SurveySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    survey_title = serializers.CharField(source="survey.title", read_only=True)

    class Meta:
        model = SurveyResponse
        fields = ['id', 'survey', 'created_by', 'created_at', 'cantine', 'answers', 'survey_title']
        # extra_kwargs = {'created_by': {"read_only": True}}
    



class NoteSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    class Meta:
        model = Note
        # survey = SurveySerializer(read_only=True)
        fields = ['id', 'title', 'content', 'categories', 'created_at', 'author', 'file']
        extra_kwargs = {'author': {"read_only": True}}
    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    # def create(self, validated_data):
    #     # Set the author to the currently logged-in user
    #     validated_data['author'] = self.context['request'].user
    #     return super().create(validated_data)