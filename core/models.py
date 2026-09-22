from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Election(models.Model):
    title = models.CharField(max_length=200, default="Главное голосование")
    blue_name = models.CharField(max_length=100, default="Синяя команда")
    red_name = models.CharField(max_length=100, default="Красная команда")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def blue_votes(self):
        return self.votes.filter(team="blue").count()

    @property
    def red_votes(self):
        return self.votes.filter(team="red").count()

    @property
    def total_votes(self):
        return self.blue_votes + self.red_votes


class ElectionVote(models.Model):
    TEAM_CHOICES = [
        ("blue", "Синяя команда"),
        ("red", "Красная команда"),
    ]

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    session_key = models.CharField(max_length=100)
    team = models.CharField(max_length=10, choices=TEAM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["election", "session_key"],
                name="unique_election_session_vote",
            )
        ]

    def __str__(self):
        return f"{self.election} — {self.team}"


class Question(models.Model):
    TYPE_CHOICES = [
        ("choice", "Выбор варианта"),
        ("text", "Свой вариант"),
    ]

    text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="choice",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:100]


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )
    text = models.CharField(max_length=300)

    def vote_count(self):
        return self.responses.filter(option=self).count()

    def __str__(self):
        return self.text


class QuestionResponse(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    session_key = models.CharField(max_length=100)
    option = models.ForeignKey(
        QuestionOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responses",
    )
    text_answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "session_key"],
                name="unique_question_session_response",
            )
        ]

    def __str__(self):
        return f"Ответ: {self.question_id}"


class UserStyle(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="site_style",
    )
    font = models.CharField(max_length=80, default="Inter")

    def __str__(self):
        return f"{self.user.username} — {self.font}"
