from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput
from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
            "tech_stack",
            "achievement",
            "github_url",
            "external_url",
            "image",
            "year",
        ]

        labels = {
            "title": "Project Title",
            "category": "Category",
            "description": "Description",
            "tech_stack": "Tech Stack",
            "achievement": "Achievement",
            "github_url": "GitHub URL",
            "external_url": "External URL",
            "image": "Image Path",
            "year": "Year",
        }
        widgets = {
            "title": TextInput(attrs={
                "placeholder": "e.g. SIGAP",
            }),
            "category": TextInput(attrs={
                "placeholder": "e.g. AI / Data Science",
            }),
            "description": Textarea(attrs={
                "placeholder": "Describe your project...",
                "rows": 5,
            }),
            "tech_stack": TextInput(attrs={
                "placeholder": "e.g. Python, Django, PostgreSQL",
            }),
            "achievement": TextInput(attrs={
                "placeholder": "e.g. Top 10 Nasional",
            }),
            "github_url": URLInput(attrs={
                "placeholder": "https://github.com/...",
            }),
            "external_url": URLInput(attrs={
                "placeholder": "https://...",
            }),
            "image": TextInput(attrs={
                "placeholder": "img/project-name.png",
            }),
            "year": NumberInput(attrs={
                "placeholder": "2026",
            }),
        }

                

