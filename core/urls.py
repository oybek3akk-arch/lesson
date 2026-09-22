from django.urls import path

from . import views

urlpatterns = [
    path("", views.splash, name="splash"),
    path("home/", views.home, name="home"),
    path("vote/", views.vote, name="vote"),

    path("api/election-results/", views.election_results, name="election_results"),
    path("vote/cast/", views.cast_vote, name="cast_vote"),
    path(
        "question/<int:question_id>/answer/",
        views.answer_question,
        name="answer_question",
    ),

    path(
        "admin-panel/login/",
        views.admin_login_view,
        name="admin_login",
    ),
    path(
        "admin-panel/",
        views.admin_panel,
        name="admin_panel",
    ),
    path(
        "admin-panel/election/create/",
        views.admin_create_election,
        name="admin_create_election",
    ),
    path(
        "admin-panel/election/<int:election_id>/toggle/",
        views.admin_toggle_election,
        name="admin_toggle_election",
    ),
    path(
        "admin-panel/question/create/",
        views.admin_create_question,
        name="admin_create_question",
    ),
    path(
        "admin-panel/question/<int:question_id>/delete/",
        views.admin_delete_question,
        name="admin_delete_question",
    ),
    path(
        "admin-panel/logout/",
        views.admin_logout,
        name="admin_logout",
    ),
]
