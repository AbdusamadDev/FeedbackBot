from django.utils.html import format_html
from django.contrib import admin

from api.models import FAQ, Category, User, Regions, Question, Answer


class UserAdmin(admin.ModelAdmin):
    search_fields = ("fullname", "region")
    ordering = ("fullname",)
    list_display = [field.name for field in User._meta.fields]
    list_filter = [field.name for field in User._meta.fields]

    def formatted_phone(self, obj):
        return f"{obj.phone_number[:4]}-{obj.phone_number[4:]}"

    formatted_phone.short_description = "Phone"


class CategoryAdmin(admin.ModelAdmin):
    exclude = ("admin",)  # Exclude the admin field from the form
    list_display = [field.name for field in Category._meta.fields]
    list_filter = [field.name for field in Category._meta.fields]

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
    list_display = [field.name for field in FAQ._meta.fields]
    list_filter = [field.name for field in FAQ._meta.fields]
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


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "status",
        "category",
        "user",
    )  # Fields to display in the admin list view
    list_filter = (
        "status",
        "category",
        "user",
    )  # Fields to filter by in the admin list view
    search_fields = ("text",)


class AnswerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Answer._meta.fields]
    list_filter = [field.name for field in Answer._meta.fields]


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Regions)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
