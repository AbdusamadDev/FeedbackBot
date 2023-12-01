from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    QuestionViewSet,
    FAQViewSet,
    AnswerViewSet,
)


router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"faqs", FAQViewSet)
router.register(r"answers", AnswerViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
8