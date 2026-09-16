import os

from django.shortcuts import render

from main.models import Experience, Project
from main.forms import ProjectForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
def check_secret(request):
    secret = os.getenv("PROJECT_SECRET")
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

def show_experience(request):
        context = {
        "name": "Muhammad Akmal Haqqani",
        "experience_list": Experience.objects.all(),
        }
        return render(request, "experience.html", context)

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

