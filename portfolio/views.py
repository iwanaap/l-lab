import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactInquiryForm
from .models import Project


logger = logging.getLogger(__name__)


AUTOMATION_EXAMPLES = [
    {
        "category": "Ventas",
        "title": "Formulario a lead y seguimiento",
        "description": "Cuando llega un formulario, crea el contacto, asigna un responsable y agenda el próximo seguimiento.",
        "result": "Cada consulta entra al flujo comercial con un próximo paso visible.",
        "technologies": ["Formularios", "CRM", "Email", "ERP"],
    },
    {
        "category": "Operación",
        "title": "Cotización a orden interna",
        "description": "Cuando se aprueba una cotización, genera una orden interna con los datos del cliente, alcance y responsables.",
        "result": "El trabajo puede comenzar sin volver a copiar la información comercial.",
        "technologies": ["Cotizaciones", "PDF", "ERP", "Webhooks"],
    },
    {
        "category": "Cobranza",
        "title": "Recordatorio de pago pendiente",
        "description": "Cuando un pago sigue pendiente cerca de su vencimiento, prepara o envía el recordatorio por el canal definido.",
        "result": "Cobranza consistente sin revisar fechas una por una.",
        "technologies": ["Pagos", "Email", "WhatsApp", "ERP"],
    },
    {
        "category": "Atención",
        "title": "Consultas de WhatsApp clasificadas",
        "description": "Guarda la solicitud, identifica su tipo y la deriva al responsable correcto cuando un cliente consulta.",
        "result": "Menos conversaciones perdidas y solicitudes más fáciles de encontrar.",
        "technologies": ["WhatsApp", "CRM", "Reglas", "APIs"],
    },
    {
        "category": "Equipo",
        "title": "Aviso de tareas vencidas",
        "description": "Cuando vence una tarea, notifica al responsable y deja el atraso visible para seguimiento.",
        "result": "Los pendientes críticos se detectan sin depender de la memoria.",
        "technologies": ["Tareas", "Email", "Telegram", "ERP"],
    },
    {
        "category": "Gestión",
        "title": "Reporte diario automático",
        "description": "Consolida ventas, tareas o movimientos y entrega un resumen sin preparar el reporte a mano.",
        "result": "Información operativa lista para revisar cada mañana.",
        "technologies": ["Dashboards", "Planillas", "ERP", "KPIs"],
    },
]


SERVICES = [
    {
        "title": "Web profesional",
        "description": "Una web rápida y confiable que genera confianza y formaliza tu proyecto, con información clara para una mejor comunicación.",
        "url": "/desarrollo-web/",
        "cta": "Ver solución web",
    },
    {
        "title": "Ordenamos tus operaciones",
        "description": "Conectamos la información y los procesos de tu negocio para reducir tareas manuales y trabajar con mayor claridad.",
        "url": "/sistemas/",
        "cta": "Conocer los sistemas",
    },
    {
        "title": "Sistemas para tu negocio",
        "description": "Conoce soluciones ya desarrolladas, como ERP Empresas y Aula Virtual, listas para adaptar a tus necesidades.",
        "url": "/sistemas/",
        "cta": "Ver sistemas",
    },
    {
        "title": "Automatizaciones de procesos",
        "description": "Alertas, lectura de documentos, reportes e integraciones para dejar de repetir tareas manuales.",
        "url": "/automatizaciones/",
        "cta": "Ver ejemplos",
    },
]


PROJECT_STATIC_PREVIEWS = {
    "adp-seguridad": {"image": "portfolio/images/adp-seguridad.png"},
    "ficha-clinica-renmai": {"image": "portfolio/images/renmai-ficha-clinica.png"},
    "likan-propiedades": {"image": "portfolio/images/likan-propiedades.png"},
    "ns-security": {"image": "portfolio/images/ns-security.png"},
    "rulkanis": {"image": "portfolio/images/rulkanis.png"},
    "solitario": {"video": "portfolio/videos/solitario.mp4"},
}


def attach_static_previews(projects):
    projects = list(projects)
    for project in projects:
        preview = PROJECT_STATIC_PREVIEWS.get(project.slug, {})
        project.static_image = preview.get("image", "")
        project.static_video = preview.get("video", "")
    return projects


CASE_STUDIES = [
    {
        "project_title": "ADP Seguridad",
        "image": "portfolio/images/adp-seguridad.png",
        "value_statement": "Una presencia digital más clara para respaldar prospección y contacto comercial.",
        "solution_type": "Web corporativa",
        "problem": "La empresa necesitaba presentar sus servicios de seguridad y habilitar un canal comercial profesional.",
        "solution": "Se diseñó y desarrolló una plataforma web enfocada en explicar la oferta y facilitar el contacto.",
        "built": "Sitio corporativo, arquitectura de contenidos, páginas de servicios y llamados a la acción.",
        "benefit": "Presencia digital propia y un punto central para respaldar la prospección comercial.",
    },
    {
        "project_title": "Ficha Clínica Renmai",
        "display_title": "Renmai",
        "image": "portfolio/images/renmai-ficha-clinica.png",
        "value_statement": "Una herramienta privada para ordenar información clínica en un flujo web dedicado.",
        "solution_type": "Sistema privado",
        "problem": "La gestión de información clínica requería un espacio privado, ordenado y accesible vía web.",
        "solution": "Se construyó una aplicación web separada del sitio público para apoyar el flujo interno.",
        "built": "Subdominio privado, fichas de información y flujo de gestión web.",
        "benefit": "Información clínica centralizada en una herramienta dedicada al proceso.",
    },
    {
        "project_title": "Likan Propiedades",
        "image": "portfolio/images/likan-propiedades.png",
        "value_statement": "Un catálogo inmobiliario propio para mostrar propiedades y recibir consultas más ordenadas.",
        "solution_type": "Catálogo inmobiliario",
        "problem": "La oferta inmobiliaria necesitaba exhibirse de forma clara y conectar cada propiedad con consultas de potenciales clientes.",
        "solution": "Se desarrolló un sitio inmobiliario para publicar propiedades y facilitar el contacto.",
        "built": "Catálogo de propiedades, fichas, navegación y canales de consulta.",
        "benefit": "Un catálogo web propio para mostrar la oferta y recibir contactos de manera más ordenada.",
    },
]


def systems(request):
    return render(request, "portfolio/systems.html")


def erp(request):
    return render(request, "portfolio/erp.html")


def web_development_projects(request):
    published_projects = Project.objects.filter(status="published")
    projects = attach_static_previews(published_projects.exclude(title__iexact="Solitario"))
    lab_projects = attach_static_previews(published_projects.filter(title__iexact="Solitario"))
    return render(
        request,
        "portfolio/web_development_projects.html",
        {"projects": projects, "lab_projects": lab_projects},
    )


def catalog(request):
    return render(request, "portfolio/catalog.html")


def automations(request):
    return render(request, "portfolio/automations.html", {"automation_examples": AUTOMATION_EXAMPLES})


def projects_hub(request):
    return redirect("/desarrollo-web/#galeria")


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def home(request):
    project_lookup = {
        project.title: project
        for project in Project.objects.filter(
            status="published",
            title__in=[case["project_title"] for case in CASE_STUDIES],
        )
    }
    case_studies = [
        {**case, "project": project_lookup.get(case["project_title"])}
        for case in CASE_STUDIES
    ]
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
            "services": SERVICES,
            "case_studies": case_studies,
            "form": form,
        },
    )
