from django import forms
from .models import Answer, Question


class AnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(
        queryset=Question.objects.filter(answer__isnull=True),
        label="Unanswered Questions",
        help_text="Select a question to answer",
    )

    class Meta:
        model = Answer
        fields = ["question", "text"]

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.question:
            self.fields["question"].queryset = Question.objects.filter(
                answer__isnull=True
            ) | Question.objects.filter(pk=self.instance.question.pk)
