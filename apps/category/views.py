from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer
from rest_framework import permissions

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permissions_classes = None


    def get_permissions(self, permission_classes=None):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in self.permission_classes]

