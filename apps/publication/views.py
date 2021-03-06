from rest_framework.viewsets import ModelViewSet
from .models import Publication
from .serializers import PublicationsSerializer
from rest_framework import permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# from .filters import PublicationDateFilter



class PublicationViewSet(ModelViewSet):
    queryset = Publication.objects.filter(published=True)
    serializer_class = PublicationsSerializer
    # filterset_class = PublicationDateFilter
    filterset_fields = ['category', 'author']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']

    def retrieve(self, request, *args, **kwargs):
        'publications'
        publication = self.get_object()
        publication.views_count +=1
        publication.save()
        return super(PublicationViewSet, self).retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = ['permission']
        return [permissions() for permissions in self.permission_classes]


