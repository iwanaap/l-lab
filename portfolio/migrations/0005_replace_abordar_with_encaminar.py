from django.db import migrations


ENCAMINAR_DEFAULTS = {
    "title": "Encaminar",
    "short_description": "Sitio web para tarotista, diseñado para presentar sus servicios y facilitar el contacto con sus consultantes.",
    "description": "Sitio web desarrollado para una tarotista, con una presentación clara de sus servicios y canales de contacto.",
    "technologies": "Django, Tailwind, HTML, CSS, JavaScript",
    "project_url": "https://encaminar.cl",
    "status": "published",
}


def replace_abordar_with_encaminar(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    abordar = Project.objects.filter(slug="abordar").first()
    encaminar = Project.objects.filter(slug="encaminar").first()

    if encaminar:
        Project.objects.filter(pk=encaminar.pk).update(**ENCAMINAR_DEFAULTS)
        Project.objects.filter(slug="abordar").delete()
    elif abordar:
        Project.objects.filter(pk=abordar.pk).update(slug="encaminar", **ENCAMINAR_DEFAULTS)
    else:
        Project.objects.create(slug="encaminar", **ENCAMINAR_DEFAULTS)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0004_update_adp_project_image"),
    ]

    operations = [
        migrations.RunPython(replace_abordar_with_encaminar, migrations.RunPython.noop),
    ]
