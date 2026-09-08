from django.db import models

# Create your models here.
import uuid
from django.db import models
class Experience(models.Model):
    EXPERIENCE_CHOICES = [
    ('internship', 'Internship'),
    ('research', 'Research'),
    ('volunteer', 'Volunteer'),
    ('part-time', 'Part-Time'),
    ('full-time', 'Full-Time'),
    ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveBigIntegerField(default=0)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    period = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(max_length=255, help_text ="Pisahkan dengan koma")

    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES,
    default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split]
    @property
    def is_ongoing(self):
        return self.ended_at is None
    