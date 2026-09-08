from django.shortcuts import render

from main.models import Experience
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