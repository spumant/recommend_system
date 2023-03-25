from django.shortcuts import render
# Create your views here.
from rest_framework.generics import GenericAPIView
from APP01.models import Special
from APP01.serializers import Special_serializer
from rest_framework.response import Response
from rest_framework import status


class recommend(GenericAPIView):
    queryset = Special.objects.all()
    serializer_class = Special_serializer

    def get(self, request, pk):
        pass
