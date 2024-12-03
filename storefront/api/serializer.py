from rest_framework import serializers
from .models import Note, User, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'categories', 'created_at', 'author', 'file']
        extra_kwargs = {'author': {"read_only": True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
    # def create(self, validated_data):
    #     # Set the author to the currently logged-in user
    #     validated_data['author'] = self.context['request'].user
    #     return super().create(validated_data)