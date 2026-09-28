from django.shortcuts import render


def landing_page(request):
    return render(request, "index.html")


def permission_denied(request, exception):
    return render(
        request,
        "403.html",
        {"name": "Muhammad Akmal Haqqani"},
        status=403,
    )
