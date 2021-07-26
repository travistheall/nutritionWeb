from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MainDesc


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainDesc
        fields = ['food_code', 'main_food_description']

