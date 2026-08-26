from django.db import migrations


ADP_IMAGE = "adpseguridad.cl_.png"


def update_adp_project_image(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(slug="adp-seguridad").update(image=ADP_IMAGE)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0003_update_rulkanis_project"),
    ]

    operations = [
        migrations.RunPython(update_adp_project_image, migrations.RunPython.noop),
    ]
