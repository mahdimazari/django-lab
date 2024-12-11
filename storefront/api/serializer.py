from rest_framework import serializers
from .models import Note, User, Category, Survey, Question, Answer, SurveyResponse, Choice



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
        fields = ['id', 'title', 'description', 'questions']
        # extra_kwargs = {'created_by': {"read_only": True}}

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['id', 'survey', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'response', 'question', 'text', 'choice']

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