from rest_framework.viewsets import ModelViewSet

from api.models import Admin
from api.serializers import AdminSerializer


class AdminViewSet(ModelViewSet):
    model = Admin
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
