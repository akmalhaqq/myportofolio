from django.db import migrations


def create_editor_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    database = schema_editor.connection.alias

    content_type, _ = ContentType.objects.using(database).get_or_create(
        app_label="main",
        model="experience",
    )
    permission, _ = Permission.objects.using(database).get_or_create(
        content_type=content_type,
        codename="change_experience",
        defaults={"name": "Can change experience"},
    )
    editor_group, _ = Group.objects.using(database).get_or_create(name="Editor")
    editor_group.permissions.add(permission)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("main", "0008_experience_starred_by"),
    ]

    operations = [
        migrations.RunPython(create_editor_group, migrations.RunPython.noop),
    ]
