from django.contrib.admin.views.main import ChangeList
from django.utils.html import format_html
from django.contrib import admin
from django.urls import reverse

from api.models import (
    FAQ,
    Category,
    Question,
    User,
    Answer,
)


class QuestionChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super().get_results(*args, **kwargs)
        for obj in self.result_list:
            obj.css_class = self.model_admin.row_classes(
                obj, self.result_list.index(obj)
            )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text_display", "question", "admin")
    fields = (
        "text",
        "question",
    )  # Explicitly define the fields to be displayed in the form

    def text_display(self, obj):
        return format_html(
            "<div style='max-width: 600px; word-wrap: break-word;'>{}</div>", obj.text
        )

    text_display.short_description = "Text"

    def get_form(self, request, obj=None, **kwargs):
        form = super(AnswerAdmin, self).get_form(request, obj, **kwargs)
        question_id = request.GET.get('question')
        if question_id and 'question' in form.base_fields:
            try:
                question_id = int(question_id)
                form.base_fields['question'].initial = question_id
            except (ValueError, TypeError):
                pass  # In case of an invalid question ID, do nothing
        return form

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        question_id = request.GET.get("question")
        if question_id:
            initial["question"] = question_id
        return initial

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new object
            obj.admin = request.user
        super().save_model(request, obj, form, change)
        # Set the Question's status to True for answered after saving the Answer
        obj.question.status = True
        obj.question.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(status=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "status", "category", "user", "answer_link")

    class Media:
        css = {
            "all": (
                "css/status.css",
            )  # The path should be inside your static directory
        }

    def changelist_view(self, request, extra_context=None):
        self.ChangeList = QuestionChangeList
        return super().changelist_view(request, extra_context)

    def row_classes(self, obj, index):
        if obj.status:  # If the question is answered
            return "row-answered"
        return "row-not-answered"

    def answer_link(self, obj):
        # This method returns a button to the add Answer page with the question preselected
        link = reverse("admin:api_answer_add") + f"?question={obj.pk}"
        return format_html(
            '<a href="{}" class="button">Answer to this Question</a>', link
        )

    answer_link.short_description = "Answer this question"

    def get_queryset(self, request):
        # Overriding get_queryset to only show unanswered questions if not superuser
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(status=False)


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
admin.site.register(Question, QuestionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Answer, AnswerAdmin)
