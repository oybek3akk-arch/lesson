from django import forms
from .models import Election, Question, QuestionOption


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ["title", "blue_name", "red_name"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Название голосования",
            }),
            "blue_name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Название синей команды",
            }),
            "red_name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Название красной команды",
            }),
        }


class QuestionForm(forms.ModelForm):
    options_text = forms.CharField(
        required=False,
        label="Варианты ответа",
        widget=forms.Textarea(attrs={
            "class": "input",
            "rows": 4,
            "placeholder": "Каждый вариант с новой строки",
        }),
    )

    class Meta:
        model = Question
        fields = ["text", "question_type", "is_active"]
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "input",
                "rows": 3,
                "placeholder": "Введите вопрос...",
            }),
            "question_type": forms.Select(attrs={"class": "input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "checkbox"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("question_type") == "choice":
            raw = cleaned.get("options_text", "")
            options = [x.strip() for x in raw.splitlines() if x.strip()]
            if len(options) < 2:
                raise forms.ValidationError(
                    "Для вопроса с вариантами добавьте минимум 2 варианта."
                )
        return cleaned

    def save(self, commit=True):
        question = super().save(commit=commit)
        if commit and question.question_type == "choice":
            question.options.all().delete()
            raw = self.cleaned_data.get("options_text", "")
            for option in raw.splitlines():
                option = option.strip()
                if option:
                    QuestionOption.objects.create(
                        question=question,
                        text=option,
                    )
        return question
