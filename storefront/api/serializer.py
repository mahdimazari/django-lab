from rest_framework import serializers
from .models import Note, User, Category,  Canteen
from djf_surveys.models import Survey



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user



class SurveySerializer(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True, read_only=True)
    print('survey model', Survey)
    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'slug']
        # extra_kwargs = {'created_by': {"read_only": True}}


class CanteenSerializer(serializers.ModelSerializer):
    admins = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    consumers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    relatedSurveys = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Canteen
        fields = ['id', 'name', 'region', 'city', 'postal_code', 'daily_meal_count', 'admins', 'consumers', 'relatedSurveys']





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