from django.urls import path

from .views import automations, erp, home, projects_hub, web_development_projects

urlpatterns = [
    path("", home, name="home"),
    path("erp/", erp, name="erp"),
    path("proyectos/", projects_hub, name="projects_hub"),
    path("desarrollo-web/", web_development_projects, name="web_development_projects"),
    path("automatizaciones/", automations, name="automations"),
]
