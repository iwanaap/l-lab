from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("published", "Publicado"),
    ]

    title = models.CharField("título", max_length=160)
    slug = models.SlugField("slug", max_length=180, unique=True, blank=True)
    short_description = models.CharField("descripción breve", max_length=240)
    description = models.TextField("descripción", blank=True)
    technologies = models.CharField(
        "tecnologías",
        max_length=240,
        blank=True,
        help_text="Separadas por coma. Ej: Django, Tailwind, PostgreSQL",
    )
    client = models.CharField("cliente", max_length=120, blank=True)
    project_url = models.URLField("URL del proyecto", blank=True)
    repository_url = models.URLField("URL del repositorio", blank=True)
    image = models.FileField("imagen", upload_to="projects/", blank=True, null=True)
    preview_video = models.FileField("video preview", upload_to="projects/videos/", blank=True, null=True)
    status = models.CharField("estado", max_length=20, choices=STATUS_CHOICES, default="draft")
    featured = models.BooleanField("destacado", default=False)
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        ordering = ["-featured", "-created_at"]
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def technology_list(self):
        return [tech.strip() for tech in self.technologies.split(",") if tech.strip()]


class ContactInquiry(models.Model):
    name = models.CharField("nombre", max_length=120)
    email = models.EmailField("email")
    phone = models.CharField("teléfono", max_length=40, blank=True)
    service = models.CharField("servicio", max_length=120, blank=True)
    message = models.TextField("mensaje")
    created_at = models.DateTimeField("creado", auto_now_add=True)
    is_read = models.BooleanField("leído", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "consulta"
        verbose_name_plural = "consultas"

    def __str__(self):
        return f"{self.name} - {self.email}"
