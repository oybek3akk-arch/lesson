from django.contrib import admin
from .models import (
    Election,
    ElectionVote,
    Question,
    QuestionOption,
    QuestionResponse,
    UserStyle,
)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text_short", "question_type", "is_active", "created_at")
    list_filter = ("question_type", "is_active")
    inlines = [QuestionOptionInline]

    @admin.display(description="Вопрос")
    def text_short(self, obj):
        return obj.text[:80]


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "blue_name",
        "red_name",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)


@admin.register(ElectionVote)
class ElectionVoteAdmin(admin.ModelAdmin):
    list_display = ("election", "team", "session_key", "created_at")
    list_filter = ("team", "election")
    readonly_fields = ("election", "team", "session_key", "created_at")


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ("question", "option", "text_answer_short", "created_at")
    readonly_fields = ("question", "session_key", "option", "text_answer", "created_at")

    @admin.display(description="Текстовый ответ")
    def text_answer_short(self, obj):
        return obj.text_answer[:80]


@admin.register(UserStyle)
class UserStyleAdmin(admin.ModelAdmin):
    list_display = ("user", "font")
