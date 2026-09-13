from django.db import models

# Create your models here.
import uuid
from django.db import models
class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveBigIntegerField(default=0)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    period = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(max_length=255, help_text ="Pisahkan dengan koma")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
    
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",")]

class Project(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    order = models.PositiveBigIntegerField(default=0)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()

    tech_stack = models.CharField(
        max_length=255,
        help_text="Pisahkan dengan koma"
    )
    achievement = models.CharField(
        max_length=255,
        blank=True
    )
    github_url = models.URLField(
        blank=True
    )
    external_url = models.URLField(
        blank=True
    )
    image = models.CharField(
        max_length=255,
        blank=True
    )
    year = models.PositiveIntegerField()

    class Meta:
        ordering=["order"]

    def __str__(self):
        return self.title
    def tech_list(self):
        return [
            tech.strip()
            for tech in self.tech_stack.split(",")
            
        ]