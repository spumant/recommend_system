from APP01.models import Collection, Like, Log, Question, Special, Users, Week, Wrong, Item
from rest_framework import serializers
from rest_framework_mongoengine import serializers as s1


class Item_serializer(s1.DocumentSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class Collection_serializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class Like_serializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class Log_serializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class Question_serializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class Special_serializer(serializers.ModelSerializer):
    class Meta:
        model = Special
        fields = '__all__'


class Users_serializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class Week_serializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = '__all__'


class Wrong_serializer(serializers.ModelSerializer):
    class Meta:
        model = Wrong
        fields = '__all__'
