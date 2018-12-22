from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class OpenView(APIView):

    def get(self, request):
        content = {'message': 'Cualquiera'}
        return Response(content)

class AdminView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Solo Admin!'}
        return Response(content)
