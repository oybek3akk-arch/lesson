import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ElectionForm, QuestionForm
from .models import (
    Election,
    ElectionVote,
    Question,
    QuestionOption,
    QuestionResponse,
    UserStyle,
)

FONTS = [
    "Inter",
    "Poppins",
    "Montserrat",
    "Playfair Display",
    "Raleway",
    "Roboto",
    "Space Grotesk",
    "DM Sans",
]


def site_visual(request):
    if not request.session.get("site_font"):
        request.session["site_font"] = random.choice(FONTS)
    return request.session["site_font"]

def site_font(request):
    return site_visual(request)


def ensure_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def splash(request):
    return render(
        request,
        "splash.html",
        {"font": site_font(request)},
    )


def home(request):
    questions = (
        Question.objects
        .filter(is_active=True)
        .prefetch_related("options")
    )

    return render(
        request,
        "home.html",
        {
            "font": site_font(request),
            "questions": questions,
        },
    )


def vote(request):
    election = Election.objects.filter(is_active=True).first()

    return render(
        request,
        "vote.html",
        {
            "font": site_font(request),
            "election": election,
        },
    )


@require_POST
def cast_vote(request):
    election = Election.objects.filter(is_active=True).first()

    if not election:
        return JsonResponse({
            "success": False,
            "message": "Сейчас активного голосования нет.",
        })

    session_key = ensure_session_key(request)
    team = request.POST.get("team")

    if team not in {"blue", "red"}:
        return JsonResponse({
            "success": False,
            "message": "Выберите команду.",
        })

    try:
        ElectionVote.objects.create(
            election=election,
            session_key=session_key,
            team=team,
        )
    except IntegrityError:
        return JsonResponse({
            "success": False,
            "message": "Вы уже проголосовали в этом голосовании.",
        })

    return election_result_json(election)


def election_result_json(election):
    blue = election.blue_votes
    red = election.red_votes
    total = blue + red

    return JsonResponse({
        "success": True,
        "blue": blue,
        "red": red,
        "total": total,
        "blue_percent": round(blue / total * 100, 1) if total else 0,
        "red_percent": round(red / total * 100, 1) if total else 0,
    })


def election_results(request):
    election = Election.objects.filter(is_active=True).first()

    if not election:
        return JsonResponse({"active": False})

    return election_result_json(election)


@require_POST
def answer_question(request, question_id):
    question = get_object_or_404(
        Question.objects.prefetch_related("options"),
        id=question_id,
        is_active=True,
    )

    session_key = ensure_session_key(request)

    if QuestionResponse.objects.filter(
        question=question,
        session_key=session_key,
    ).exists():
        return JsonResponse({
            "success": False,
            "message": "Вы уже ответили на этот вопрос.",
        })

    if question.question_type == "choice":
        option_id = request.POST.get("option")
        option = get_object_or_404(
            QuestionOption,
            id=option_id,
            question=question,
        )

        QuestionResponse.objects.create(
            question=question,
            session_key=session_key,
            option=option,
        )

    else:
        text = request.POST.get("text", "").strip()

        if not text:
            return JsonResponse({
                "success": False,
                "message": "Напишите свой вариант.",
            })

        QuestionResponse.objects.create(
            question=question,
            session_key=session_key,
            text_answer=text,
        )

    return JsonResponse({"success": True})


def staff_check(user):
    return user.is_authenticated and user.is_staff


def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_panel")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_panel")

        messages.error(
            request,
            "Неверный логин, пароль или недостаточно прав.",
        )

    return render(
        request,
        "admin_login.html",
        {"font": site_font(request)},
    )


@login_required(login_url="/admin-panel/login/")
@user_passes_test(staff_check, login_url="/admin-panel/login/")
def admin_panel(request):
    election = Election.objects.filter(is_active=True).first()
    elections = Election.objects.all()

    questions = (
        Question.objects
        .prefetch_related("options", "responses")
        .all()
    )

    return render(
        request,
        "admin.html",
        {
            "font": site_font(request),
            "active_election": election,
            "elections": elections,
            "questions": questions,
            "election_form": ElectionForm(),
            "question_form": QuestionForm(),
        },
    )


@login_required(login_url="/admin-panel/login/")
@user_passes_test(staff_check, login_url="/admin-panel/login/")
@require_POST
def admin_create_election(request):
    form = ElectionForm(request.POST)

    if form.is_valid():
        Election.objects.update(is_active=False)
        election = form.save()
        election.is_active = True
        election.save(update_fields=["is_active"])
        messages.success(request, "Новое голосование создано.")
    else:
        messages.error(request, "Проверьте данные голосования.")

    return redirect("admin_panel")


@login_required(login_url="/admin-panel/login/")
@user_passes_test(staff_check, login_url="/admin-panel/login/")
@require_POST
def admin_toggle_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    if election.is_active:
        election.is_active = False
        election.save(update_fields=["is_active"])
    else:
        Election.objects.update(is_active=False)
        election.is_active = True
        election.save(update_fields=["is_active"])

    return redirect("admin_panel")


@login_required(login_url="/admin-panel/login/")
@user_passes_test(staff_check, login_url="/admin-panel/login/")
@require_POST
def admin_create_question(request):
    form = QuestionForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Вопрос добавлен.")
    else:
        messages.error(
            request,
            "Не удалось добавить вопрос. Проверьте варианты ответа.",
        )

    return redirect("admin_panel")


@login_required(login_url="/admin-panel/login/")
@user_passes_test(staff_check, login_url="/admin-panel/login/")
@require_POST
def admin_delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, "Вопрос удален.")
    return redirect("admin_panel")
