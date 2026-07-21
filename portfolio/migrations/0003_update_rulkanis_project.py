from django.db import migrations


RULKANIS_DESCRIPTION = "Juego de cartas desarrollado por l-lab, ¡visita nuestro proyecto!"


def update_rulkanis_project(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.update_or_create(
        slug="rulkanis",
        defaults={
            "title": "Rulkanis",
            "short_description": RULKANIS_DESCRIPTION,
            "description": RULKANIS_DESCRIPTION,
            "project_url": "https://rulkanis.l-lab.cl",
            "image": "rulkanis.l-lab.cl_.png",
            "status": "published",
            "featured": True,
            "technologies": "Django, Tailwind, HTML, CSS, JavaScript",
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_project_preview_video"),
    ]

    operations = [
        migrations.RunPython(update_rulkanis_project, migrations.RunPython.noop),
    ]
