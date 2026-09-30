from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput
from django.utils.html import strip_tags
from main.models import Project, Experience


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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "category",            
            "title",
            "company",
            "period",
            "description",
            "tags",
        ]

                

