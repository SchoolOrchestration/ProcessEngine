from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers, viewsets, routers
from processengine.models import Process


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'
        ordering = ('created_date',)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProcessViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


router = routers.DefaultRouter()
router.register(r'process', ProcessViewSet)