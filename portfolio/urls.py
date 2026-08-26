from django.urls import path

from .views import automations, catalog, erp, home, projects_hub, systems, web_development_projects

urlpatterns = [
    path("", home, name="home"),
    path("sistemas/", systems, name="systems"),
    path("erp/", erp, name="erp"),
    path("proyectos/", projects_hub, name="projects_hub"),
    path("desarrollo-web/", web_development_projects, name="web_development_projects"),
    path("catalogo-web/", catalog, name="catalog"),
    path("automatizaciones/", automations, name="automations"),
]
