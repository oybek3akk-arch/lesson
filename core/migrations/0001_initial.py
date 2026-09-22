from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Election",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Главное голосование", max_length=200)),
                ("blue_name", models.CharField(default="Синяя команда", max_length=100)),
                ("red_name", models.CharField(default="Красная команда", max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("question_type", models.CharField(
                    choices=[("choice", "Выбор варианта"), ("text", "Свой вариант")],
                    default="choice",
                    max_length=20,
                )),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="QuestionOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=300)),
                ("question", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="options",
                    to="core.question",
                )),
            ],
        ),
        migrations.CreateModel(
            name="ElectionVote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(max_length=100)),
                ("team", models.CharField(
                    choices=[("blue", "Синяя команда"), ("red", "Красная команда")],
                    max_length=10,
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("election", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="votes",
                    to="core.election",
                )),
            ],
        ),
        migrations.CreateModel(
            name="QuestionResponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(max_length=100)),
                ("text_answer", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("option", models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name="responses",
                    to="core.questionoption",
                )),
                ("question", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="responses",
                    to="core.question",
                )),
            ],
        ),
        migrations.CreateModel(
            name="UserStyle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("font", models.CharField(default="Inter", max_length=80)),
                ("user", models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="site_style",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.AddConstraint(
            model_name="electionvote",
            constraint=models.UniqueConstraint(
                fields=("election", "session_key"),
                name="unique_election_session_vote",
            ),
        ),
        migrations.AddConstraint(
            model_name="questionresponse",
            constraint=models.UniqueConstraint(
                fields=("question", "session_key"),
                name="unique_question_session_response",
            ),
        ),
    ]
