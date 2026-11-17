from urllib.parse import urlencode

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactInquiryForm
from .models import Project


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
        "eyebrow": "Vender mejor",
        "title": "Consigue más consultas",
        "description": "Una presencia digital clara para que tus clientes entiendan qué haces, confíen y sepan cómo contactarte.",
        "examples": "Web corporativa · catálogo · landing page",
        "url": "#contacto",
        "cta": "Quiero mejorar mi web",
    },
    {
        "eyebrow": "Trabajar con orden",
        "title": "Centraliza tu operación",
        "description": "Un sistema pensado según tu forma de trabajar para tener clientes, ventas, tareas y documentos en un solo lugar.",
        "examples": "ERP · gestión interna · plataforma privada",
        "url": "#contacto",
        "cta": "Quiero ordenar mi negocio",
    },
    {
        "eyebrow": "Ahorrar tiempo",
        "title": "Deja de repetir tareas",
        "description": "Conectamos tus herramientas y automatizamos pasos manuales para reducir errores y liberar tiempo de tu equipo.",
        "examples": "Alertas · reportes · documentos · integraciones",
        "url": "#contacto",
        "cta": "Quiero automatizar un proceso",
    },
]


PROJECT_STATIC_PREVIEWS = {
    "adp-seguridad": {"image": "portfolio/images/adp-seguridad.png"},
    "encaminar": {"image": "portfolio/images/encaminar.png"},
    "ficha-clinica-renmai": {"image": "portfolio/images/renmai-ficha-clinica.png"},
    "ns-security": {"image": "portfolio/images/ns-security.png"},
    "renmai": {"image": "portfolio/images/renmai.png"},
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
        "url": "https://adpseguridad.cl",
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
        "url": "https://fichaclinica.renmai.cl",
        "image": "portfolio/images/renmai-ficha-clinica.png",
        "value_statement": "Una herramienta privada para ordenar información clínica en un flujo web dedicado.",
        "solution_type": "Sistema privado",
        "problem": "La gestión de información clínica requería un espacio privado, ordenado y accesible vía web.",
        "solution": "Se construyó una aplicación web separada del sitio público para apoyar el flujo interno.",
        "built": "Subdominio privado, fichas de información y flujo de gestión web.",
        "benefit": "Información clínica centralizada en una herramienta dedicada al proceso.",
    },
]


def systems(request):
    return render(request, "portfolio/systems.html")


def erp(request):
    return render(request, "portfolio/erp.html")


def web_development_projects(request):
    published_projects = Project.objects.filter(status="published")
    projects = attach_static_previews(
        published_projects.exclude(title__iexact="Solitario")
        .exclude(slug="ficha-clinica-renmai")
        .exclude(slug="likan-propiedades")
    )
    showcase_projects = [project for project in projects if project.static_image or project.image]
    lab_projects = attach_static_previews(published_projects.filter(title__iexact="Solitario"))
    return render(
        request,
        "portfolio/web_development_projects.html",
        {
            "projects": projects,
            "showcase_projects": showcase_projects,
            "lab_projects": lab_projects,
        },
    )


def catalog(request):
    return render(request, "portfolio/catalog.html")


def automations(request):
    return render(request, "portfolio/automations.html", {"automation_examples": AUTOMATION_EXAMPLES})


def projects_hub(request):
    return redirect("/#casos", permanent=True)


def legacy_page_redirect(request):
    """Keep old page URLs useful while the public site operates as one landing page."""
    destinations = {
        "/sistemas/": "/#soluciones",
        "/erp/": "/#soluciones",
        "/desarrollo-web/": "/#casos",
        "/catalogo-web/": "/#soluciones",
        "/automatizaciones/": "/#soluciones",
    }
    return redirect(destinations.get(request.path, "/"), permanent=True)


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
            data = form.cleaned_data
            whatsapp_message = (
                "Hola l-lab, quiero agendar un diagnóstico.\n\n"
                f"Nombre: {data['name']}\n"
                f"Teléfono: {data['phone'] or 'No indicado'}\n"
                f"Servicio: {data['service']}\n\n"
                f"Mensaje: {data['message']}"
            )
            whatsapp_url = f"https://wa.me/56934821394?{urlencode({'text': whatsapp_message})}"
            return redirect(whatsapp_url)
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
