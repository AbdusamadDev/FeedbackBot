from django.contrib import admin
from django.utils.html import format_html
from api.models import Answer, Question, FAQ, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("detailed_description",)
    exclude = ("admin",)  # Exclude the admin field from the form

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if this is a new object being created
            # Set the admin field to the current user
            obj.admin = request.user
        super().save_model(request, obj, form, change)

    def detailed_description(self, obj):
        return format_html(
            "Title: {}<br>Admin: {}<br>Date Created: {}",
            obj.title,
            obj.admin.username,
            obj.date_created.strftime("%Y-%m-%d"),
        )

    detailed_description.short_description = "Category Details"


class FAQAdmin(admin.ModelAdmin):
    list_display = ("detailed_description",)
    exclude = ("admin",)  # Exclude the admin field from the form

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if this is a new object being created
            # Set the admin field to the current user
            obj.admin = request.user
        super().save_model(request, obj, form, change)

    def detailed_description(self, obj):
        return format_html(
            "Question: {}<br>Answer: {}<br><br>Created by {}",
            obj.question,
            obj.answer,
            obj.admin.username,
        )

    detailed_description.short_description = "FAQ Details"


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("detailed_description",)
    exclude = ("admin",)  # Exclude the admin field from the form

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if this is a new object being created
            # Set the admin field to the current user
            obj.admin = request.user
        super().save_model(request, obj, form, change)

    def detailed_description(self, obj):
        return format_html(
            "Answer Text: {}<br>Question: {}<br>Admin: {}",
            obj.text,
            obj.question.text,
            obj.admin.username,
        )

    detailed_description.short_description = "Answer Details"


admin.site.register(Category, CategoryAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Answer, AnswerAdmin)
