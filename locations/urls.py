from . import views

from django.urls import path

app_name = "locations"
urlpatterns = [
    path("", views.index, name="index"),
    path("verify", views.verify, name="verify"),
    path("delete", views.delete, name="delete"),
    path("admin-home", views.admin_homepage, name="admin_home"),
    path("add-activity", views.add_activity, name="add_activity"),
    path("add-study-space", views.add_study_space, name="add_study_space"),
    path(
        "study-space/<int:study_space_id>",
        views.study_space_view,
        name="study_space_view",
    ),
    path("activity/<int:activity_id>", views.activity_view, name="activity_view"),
    path(
        "study_space/<int:study_space_id>",
        views.study_space_view,
        name="study_space_view",
    ),
    path(
        "activity/delete/<int:activity_id>",
        views.delete_activity,
        name="activity_delete",
    ),
    path(
        "activity/modify/<int:activity_id>",
        views.modify_activity,
        name="activity_modify",
    ),
    path(
        "study_space/delete/<int:study_space_id>",
        views.delete_studyspace,
        name="study_space_delete",
    ),
    path(
        "study_space/modify/<int:study_space_id>",
        views.modify_studyspace,
        name="study_space_modify",
    ),
]
