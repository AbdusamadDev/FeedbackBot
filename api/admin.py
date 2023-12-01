from django.contrib import admin, messages
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse

from api.forms import AnswerQuestionForm
from api.models import (
    FAQ,
    Category,
    Question,
    User,
    Answer,
)


class UserAdmin(admin.ModelAdmin):
    list_display = ("fullname", "phone_number", "region", "formatted_phone")
    search_fields = ("fullname", "region")
    list_filter = ("region",)
    ordering = ("fullname",)

    def formatted_phone(self, obj):
        return f"{obj.phone_number[:4]}-{obj.phone_number[4:]}"

    formatted_phone.short_description = "Phone"


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Question)
admin.site.register(User, UserAdmin)
