from django.contrib import admin
from .models import Experience, Project
# Register your models here.

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    readonly_fields = ("order",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.order = Experience.next_order()
        super().save_model(request, obj, form, change)


admin.site.register(Project)
