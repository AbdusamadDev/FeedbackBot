from rest_framework import viewsets, permissions

from api.models import Category, User, Question, FAQ, Answer
from api.permissions import IsSuperAdmin, IsAdminUserOrReadOnly
from api.serializers import (
    CategorySerializer,
    QuestionSerializer,
    FAQSerializer,
    AnswerSerializer,
)


# ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperAdmin]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsSuperAdmin]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminUserOrReadOnly]
