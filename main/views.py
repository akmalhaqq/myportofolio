from unicodedata import category

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import override
from django.views.decorators.http import require_POST

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

def _filtered_experiences(request):
    category_query = request.GET.get("category", "").strip()
    sort_query = request.GET.get("sort", "").strip()

    experiences = Experience.objects.annotate(
        star_count=Count("starred_by")
    ).prefetch_related("starred_by")
    if category_query:
        experiences = experiences.filter(category__iexact=category_query)

    if sort_query == "a-z":
        experiences = experiences.order_by("title")
    elif sort_query == "z-a":
        experiences = experiences.order_by("-title")
    elif sort_query == "most-starred":
        experiences = experiences.order_by("-star_count", "order", "pk")
    # default is by order
    return experiences

# JSON
def get_experience_json(request):
    data = []
    for experience in _filtered_experiences(request):
        is_starred = request.user.is_authenticated and any(
            user.pk == request.user.pk for user in experience.starred_by.all()
        )
        data.append({
            "model": "main.experience",
            "pk": str(experience.pk),
            "fields": {
                "order": experience.order,
                "title": experience.title,
                "company": experience.company,
                "period": experience.period,
                "category": experience.category,
                "description": experience.description,
                "tags": experience.tags,
                "star_count": experience.star_count,
                "is_starred": is_starred,
            },
        })
    return JsonResponse(data, safe=False)

# show experience
def show_experience(request):
    experiences = _filtered_experiences(request)

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
    if not request.user.has_perm("main.change_experience"):
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


@login_required(login_url="/login/", redirect_field_name=None)
@require_POST
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    return redirect("main:show_experience")

#get project and show project
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []

    for project in projects:
        starred_users = list(project.starred_by.all())

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "category": project.category,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "achievement": project.achievement,
                "github_url": project.github_url,
                "external_url": project.external_url,
                "image": project.image,
                "year": project.year,
                "star_count": len(starred_users),
                "is_starred": (
                    request.user.is_authenticated
                    and any(user.pk == request.user.pk for user in starred_users)
                ),
                "starred_by_names": ", ".join(
                    user.username for user in starred_users
                ),
            },
        })

    return JsonResponse(data, safe=False)

def show_projects(request):
    context = {
        "name": "Muhammad Akmal Haqqani",
        "title_query": request.GET.get("title", "").strip(),
        "form":ProjectForm(),
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

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {
                "message": "Proyek berhasil ditambahkan.",
                "pk": str(project.id),
            },
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )

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
    next_url = request.POST.get("next") or request.GET.get("next", "")
    if not next_url.startswith("/") or not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ""

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        login_time_wib = timezone.localtime(timezone.now())
        with override("id"):
            login_time = f"{date_format(login_time_wib, 'j F Y, H:i:s')} WIB"
        response = redirect(next_url or "main:show_main")
        response.set_cookie("last_login", login_time, samesite="Lax")
        return response

    context = {
        "name": "Muhammad Akmal Haqqani",
        "form": form,
        "next_url": next_url,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

