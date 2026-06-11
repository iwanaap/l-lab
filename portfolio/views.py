from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactInquiryForm
from .models import Project


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


def home(request):
    projects = Project.objects.filter(status="published")[:6]
    form = ContactInquiryForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Mensaje recibido. Te contactaré pronto para revisar tu cotización.")
            return redirect("home")
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
