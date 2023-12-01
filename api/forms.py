from django import forms


class AnswerQuestionForm(forms.Form):
    _selected_action = forms.CharField(
        widget=forms.MultipleHiddenInput
    )  # Hidden field for selected questions
    answer_text = forms.CharField(
        widget=forms.Textarea, label="Answer"
    )  # Textarea for the answer

    def __init__(self, *args, **kwargs):
        super(AnswerQuestionForm, self).__init__(*args, **kwargs)
        self.fields["answer_text"].widget.attrs.update(
            {"class": "vLargeTextField", "cols": "40", "rows": "10"}
        )
