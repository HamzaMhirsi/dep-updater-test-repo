from rest_framework import viewsets, status, serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserSerializer(serializers.Serializer):
    """User serializer using deprecated fields"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    # Deprecated: NullBooleanField removed in DRF 3.14+
    is_verified = serializers.NullBooleanField(required=False)
    is_admin = serializers.NullBooleanField(required=False)


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for user management"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    serializer_class = UserSerializer

    def list(self, request):
        return Response({'users': []})

    def retrieve(self, request, pk=None):
        return Response({'user': {'id': pk}})

    # Deprecated: detail_route was removed in DRF 3.15, use @action(detail=True)
    @detail_route(methods=['post'])
    def activate(self, request, pk=None):
        return Response({'status': 'activated', 'user_id': pk})

    # Deprecated: list_route was removed in DRF 3.15, use @action(detail=False)
    @list_route(methods=['get'])
    def me(self, request):
        return Response({'user': {'id': request.user.id}})

    @detail_route(methods=['post'])
    def deactivate(self, request, pk=None):
        return Response({'status': 'deactivated', 'user_id': pk})

    @list_route(methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        return Response({'results': [], 'query': query})
