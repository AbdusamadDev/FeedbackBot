from django.http import HttpResponseRedirect
from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render
from django.urls import path, reverse

from api.forms import AnswerForm, AnswerQuestionForm
from api.models import Answer, FAQ, Category, Question


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
    form = AnswerForm
    list_display = ["question", "text"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(question__status="No")

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


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "is_answered", "user"]
    ordering = ["is_answered"]
    actions = ["answer_questions"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("answer/", self.admin_site.admin_view(self.answer_questions_view))
        ]
        return custom_urls + urls

    def answer_questions_view(self, request):
        # Handle the form submission
        if request.method == "POST":
            form = AnswerQuestionForm(request.POST)

            if form.is_valid():
                question_ids = request.POST.getlist("_selected_action")
                answer_text = form.cleaned_data["answer_text"]

                for question_id in question_ids:
                    question = Question.objects.get(pk=question_id)
                    # Logic to save the answer
                    # Update the question's status or create an Answer object, etc.

                self.message_user(request, "Questions answered successfully")
                return HttpResponseRedirect(reverse("admin:app_question_changelist"))

        else:
            form = AnswerQuestionForm(
                initial={
                    "_selected_action": request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
                }
            )

        return render(request, "admin/answer_questions.html", {"questions_form": form})

    def answer_questions(self, request, queryset):
        return HttpResponseRedirect(
            reverse("admin:app_question_answer", args=[queryset[0].id])
        )

    answer_questions.short_description = "Answer selected questions"


admin.site.register(Category, CategoryAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
