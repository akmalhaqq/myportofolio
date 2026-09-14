from django.shortcuts import render

from main.models import Experience, Project
from main.forms import ProjectForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
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

def show_projects(request):
      projects = Project.objects.all()

      context = {
            "project_list": projects,
      }

      return render(request, "projects.html", context)

def create_project(request):
      form = ProjectForm(request.POST or None)
      if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")
      context = {
            "name": "Burhan",
            "form": form,
             }
      return render(request, "projects_form.html", context)
