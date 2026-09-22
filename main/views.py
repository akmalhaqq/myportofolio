from unicodedata import category

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project

# Create your views here.
def show_main(request):
    context = {
    "name": "Muhammad Akmal Haqqani",
    "npm": "2506548295",
    "study_program": "S1 Ilmu Komputer",
    "last_login": request.COOKIES.get("last_login")
    or "Belum ada sesi login / Cookie tidak ditemukan",
    "bio": (
    "Hi, I’m Akmal, a Computer Science student at Universitas Indonesia" 
    "fascinated by AI, data, and mathematics. I like digging into"
    "problems and understanding what makes things work. This site is \
     where I share what I discover."
    ),
    }
    return render(request, "index.html", context)

# JSON 
def get_experience_json(request):
      category_query = request.GET.get("category", "").strip()
      sort_query = request.GET.get("sort", "").strip()

      experiences = Experience.objects.all()
      if category_query:
            experiences = experiences.filter(
                  category__iexact = category_query
            )

      if sort_query == "a-z":
            experiences = experiences.order_by("title")
      elif sort_query == "z-a":
            experiences = experiences.order_by("-title")
      # default is by order

      experiences_json = serializers.serialize("json", experiences)
      return HttpResponse(experiences_json, content_type="application/json")

# show experience
def show_experience(request):
        json_response = get_experience_json(request)
        experiences = serializers.deserialize("json",json_response.content.decode("utf-8"))

        experiences = [
            experience.object for experience in experiences
        ]

        category_query = request.GET.get("category", "").strip()
        sort_query = request.GET.get("sort", "").strip()
      

        context = {
        "name": "Muhammad Akmal Haqqani",
        "experience_list": experiences,
        "category_query" : category_query,
        "sort_query" : sort_query,
        }
        return render(request, "experience.html", context)

# create experience 

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        last_experience = Experience.objects.order_by("-order").first()

        if last_experience:
            form.instance.order = last_experience.order + 1
        else:
            form.instance.order = 1

        form.save()

        messages.success(
            request,
            "Experience berhasil ditambahkan!"
        )

        return redirect("main:show_experience")

    context = {
        "name": "Muhammad Akmal Haqqani",
        "form": form,
        "form_title": "Add Experience",
        "submit_label": "Tambah Experience",
        "form_action" : request.path,
    }

    return render(
        request,
        "experience_form.html",
        context
    )
# Update experience
@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Experience berhasil diperbarui!"
        )

        return redirect("main:show_experience")

    context = {
        "name": "Muhammad Akmal Haqqani",
        "form": form,
        "form_title": "Edit Experience",
        "submit_label": "Simpan Perubahan",
        "form_action": request.path,
    }

    return render(
        request,
        "experience_form.html",
        context
    )

# delete experience
@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    if request.method == "POST":
        experience.delete()
        messages.success(
            request,
            "Experience berhasil dihapus!"
        )

    return redirect("main:show_experience")

#get project and show project
def get_projects_json(request):
      title_query = request.GET.get("title", "").strip()
      projects = Project.objects.all()

      if title_query:
            projects = projects.filter(title__icontains = title_query)

      projects_json = serializers.serialize(
            "json",
            projects,
            use_natural_foreign_keys=True,
      )

      return HttpResponse(projects_json, content_type= "application/json")

def show_projects(request):
      json_response = get_projects_json(request)
      projects = serializers.deserialize(
            "json",
            json_response.content.decode("utf-8"),
            )
      
      projects = [project.object for project in projects]

      title_query = request.GET.get("title", "").strip()

      context = {
            "name":"Muhammad Akmal Haqqani",
            "project_list": projects,
            "title_query":title_query,
      }

      return render(request, "projects.html", context)
# Delete and Create Project
@login_required(login_url="/login/")
def create_project(request):
      if not request.user.is_superuser:
            raise PermissionDenied

      form = ProjectForm(request.POST or None)
      if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")

      context = {
            "name": "Muhammad Akmal Haqqani",
            "form": form,
             }
      return render(request, "projects_form.html", context)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if project.starred_by.filter(pk=request.user.pk).exists():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

# Authentication
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Muhammad Akmal Haqqani",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        login_time = timezone.localtime(timezone.now()).strftime(
            "%Y-%m-%d %H:%M:%S WIB"
        )
        response = redirect("main:show_main")
        response.set_cookie("last_login", login_time, samesite="Lax")
        return response

    context = {
        "name": "Muhammad Akmal Haqqani",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response
