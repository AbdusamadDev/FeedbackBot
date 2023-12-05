from django_filters import rest_framework as filters
from .models import User, Question, Category


class QuestionFilter(filters.FilterSet):
    region = filters.CharFilter(
        field_name="user__region"
    )  # Assuming 'region' is a field in the User model
    date = filters.DateFromToRangeFilter(
        field_name="date_created"
    )  # Replace 'date_created' with the actual date field in your model
    category = filters.CharFilter(
        field_name="category__title"
    )  # Assuming 'title' is a field in the Category model
    status = filters.BooleanFilter(
        field_name="status"
    )  # Assuming 'status' is a boolean field in your model

    class Meta:
        model = Question
        fields = ["region", "date", "category", "status"]
