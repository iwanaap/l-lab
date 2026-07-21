import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactInquiryForm
from .models import Project


logger = logging.getLogger(__name__)


AUTOMATION_PROJECTS = [
    {
        "category": "Automatización comercial",
        "title": "Seguimiento comercial automático",
        "description": "Captura prospectos desde formularios o WhatsApp, clasifica interés, crea recordatorios y evita que oportunidades queden perdidas.",
        "result": "Menos seguimiento manual y más control sobre cada contacto.",
        "technologies": ["CRM", "WhatsApp", "Email", "IA"],
        "accent": "cyan",
    },
    {
        "category": "Documentos y cotizaciones",
        "title": "Generación de propuestas",
        "description": "Sistema para ordenar datos del cliente, calcular valores, generar documentos y enviar cotizaciones con menos pasos repetitivos.",
        "result": "Cotizaciones más rápidas, consistentes y fáciles de rastrear.",
        "technologies": ["PDF", "Planillas", "Django", "Email"],
        "accent": "ember",
    },
    {
        "category": "Control operativo",
        "title": "Panel de tareas y alertas",
        "description": "Tablero para centralizar tareas, estados, responsables y alertas internas sin depender de chats dispersos.",
        "result": "Mayor visibilidad de pendientes y procesos críticos.",
        "technologies": ["Dashboard", "APIs", "Reportes", "KPIs"],
        "accent": "lime",
    },
]


SERVICES = [
    {
        "title": "Páginas web corporativas",
        "description": "Sitios sobrios, rápidos y administrables para presentar servicios, capturar clientes y construir confianza.",
    },
    {
        "title": "Landing pages",
        "description": "Páginas enfocadas en conversión para campañas, lanzamientos, validación de productos o servicios específicos.",
    },
    {
        "title": "Aplicaciones web",
        "description": "Plataformas a medida con paneles, usuarios, flujos de negocio, integraciones y despliegue productivo.",
    },
    {
        "title": "Sistemas internos",
        "description": "Herramientas privadas para ordenar operaciones, reportes, documentos, inventario, procesos y equipos.",
    },
    {
        "title": "Dashboards e integraciones",
        "description": "Visualización de datos, conexión con APIs, automatizaciones y tableros para tomar mejores decisiones.",
    },
    {
        "title": "Mantención y mejoras",
        "description": "Optimización, soporte, seguridad, evolución funcional, hosting, dominio y correo según necesidad.",
    },
]


def erp(request):
    return render(request, "portfolio/erp.html")


def web_development_projects(request):
    projects = Project.objects.filter(status="published")
    return render(request, "portfolio/web_development_projects.html", {"projects": projects})


def automations(request):
    return render(request, "portfolio/automations.html", {"automation_projects": AUTOMATION_PROJECTS})


def projects_hub(request):
    return redirect("/#proyectos")


def home(request):
    projects = Project.objects.filter(status="published")[:6]
    form = ContactInquiryForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            inquiry = form.save()
            subject = f"Nueva solicitud de contacto: {inquiry.service or 'Sin servicio'}"
            body = (
                "Se recibió una nueva solicitud desde l-lab.cl\n\n"
                f"Nombre: {inquiry.name}\n"
                f"Email: {inquiry.email}\n"
                f"Teléfono: {inquiry.phone or 'No indicado'}\n"
                f"Servicio: {inquiry.service or 'No indicado'}\n\n"
                f"Mensaje:\n{inquiry.message}\n"
            )
            try:
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[inquiry.email],
                )
                email.send(fail_silently=False)
                messages.success(request, "Mensaje enviado. Te contactaremos pronto.")
                return redirect("/?sent=1#contacto")
            except Exception:
                logger.exception("No se pudo enviar la solicitud de contacto por correo.")
                messages.error(request, "Recibimos tu solicitud, pero no se pudo enviar la notificación por correo. Te contactaré pronto.")
                return redirect("/#contacto")
        messages.error(request, "Revisa los campos del formulario e intenta nuevamente.")

    return render(
        request,
        "portfolio/home.html",
        {
            "projects": projects,
            "services": SERVICES,
            "form": form,
        },
    )
