from django.core.management.base import BaseCommand
from core.models import Election, Question, QuestionOption


class Command(BaseCommand):
    help = "Добавляет демонстрационное голосование и вопросы."

    def handle(self, *args, **options):
        election, _ = Election.objects.get_or_create(
            title="Главное голосование",
            defaults={
                "blue_name": "Синяя команда",
                "red_name": "Красная команда",
                "is_active": True,
            },
        )

        if not Question.objects.exists():
            q1 = Question.objects.create(
                text="Что для вас означает самопознание?",
                question_type="text",
            )

            q2 = Question.objects.create(
                text="Какой навык вы хотели бы развить?",
                question_type="choice",
            )

            for text in [
                "Уверенность в себе",
                "Коммуникацию",
                "Критическое мышление",
                "Умение планировать",
            ]:
                QuestionOption.objects.create(
                    question=q2,
                    text=text,
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Демонстрационные данные готовы."
            )
        )
