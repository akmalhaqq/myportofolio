import os

from django.shortcuts import render

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
def check_secret(request):
    secret = os.getenv("PROJECT_SECRET")
    if not secret:
        return False
    return request.headers.get("X-SECRET-CODE") == secret or request.POST.get("secret_code") == secret

def show_main(request):
    context = {
    "name": "Muhammad Akmal Haqqani",
    "npm": "2506548295",
    "study_program": "S1 Ilmu Komputer",
    "bio": (
    "Hi, I’m Akmal, a Computer Science student at Universitas Indonesia" 
    "fascinated by AI, data, and mathematics. I like digging into"
    "problems and understanding what makes things work. This site is \
     where I share what I discover."
    ),
    }
    return render(request, "index.html", context)
# show experience
def show_experience(request):
        context = {
        "name": "Muhammad Akmal Haqqani",
        "experience_list": Experience.objects.all(),
        }
        return render(request, "experience.html", context)

# create experience 

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if check_secret(request):
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

        else:
            messages.error(
                request,
                "Kode rahasia salah!"
            )

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
def update_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        if check_secret(request):
            form.save()

            messages.success(
                request,
                "Experience berhasil diperbarui!"
            )

            return redirect("main:show_experience")

        else:
            messages.error(
                request,
                "Kode rahasia salah!"
            )

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
def delete_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    if request.method == "POST":
        if check_secret(request):
            experience.delete()
            messages.success(
                request,
                "Experience berhasil dihapus!"
            )
        else:
            messages.error(
                request,
                "Kode rahasia salah!"
            )

    return redirect("main:show_experience")

#get project and show project
def get_projects_json(request):
      title_query = request.GET.get("title", "").strip()
      projects = Project.objects.all()

      if title_query:
            projects = projects.filter(title__icontains = title_query)

      projects_json = serializers.serialize("json", projects)

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
def create_project(request):
      form = ProjectForm(request.POST or None)
      if request.method == "POST" and form.is_valid():
            if check_secret(request):
                  form.save()
                  messages.success(request, "Proyek baru berhasil ditambahkan!")
                  return redirect("main:show_projects")
            else:
                  messages.error(request, "Kode rahasia salah!")

      context = {
            "name": "Burhan",
            "form": form,
             }
      return render(request, "projects_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if check_secret(request):
            project.delete()
            messages.success(request, "Project berhasil dihapus!")
        else:
            messages.error(request, "Kode rahasia salah!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

