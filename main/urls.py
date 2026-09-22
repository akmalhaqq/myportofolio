from unicodedata import name
from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    show_projects, 
    create_project, 
    get_projects_json, 
    delete_project,
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    login_user,
    logout_user,
    register,
    toggle_star,
    )

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name = "show_projects"),
    path("projects/add/",create_project,name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("experience/add/", create_experience, name = "create_experience"),
    path("experience/<uuid:experience_id>/update/", update_experience, name = "update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json")
]
