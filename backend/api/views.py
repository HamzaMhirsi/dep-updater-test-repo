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
    # Deprecated: list_route was removed in DRF 3.15, use @action(detail=False)
    @list_route(methods=['get'])
    def me(self, request):
        return Response({'user': {'id': request.user.id}})

    # GDPR Art. 16 — Right to Rectification
    # Authenticated users can correct their own personal data. Updates
    # are applied via the serializer (partial update) and audit-logged.
    @list_route(methods=['patch', 'put'])
    def update_me(self, request):
        import logging
        logger = logging.getLogger('gdpr.audit')

        # Whitelist fields a data subject may rectify about themselves.
        RECTIFIABLE = {'username', 'email'}
        payload = {k: v for k, v in request.data.items() if k in RECTIFIABLE}
        if not payload:
            return Response(
                {'error': 'No rectifiable fields provided'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=payload, partial=True)
        serializer.is_valid(raise_exception=True)

        # NOTE: persist via your User model + propagate to any related
        # profile/auth/marketing tables here so no data source is stale.
        # e.g. User.objects.filter(pk=request.user.id).update(**payload)

        logger.info(
            'gdpr.rectification user_id=%s fields=%s',
            getattr(request.user, 'id', None),
            list(payload.keys()),
        )
        return Response({'updated': payload, 'user_id': request.user.id})

    @detail_route(methods=['post'])
    def deactivate(self, request, pk=None):
    @detail_route(methods=['post'])
    def deactivate(self, request, pk=None):
        return Response({'status': 'deactivated', 'user_id': pk})

    @list_route(methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        return Response({'results': [], 'query': query})
