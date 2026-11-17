from django.urls import path

from .views import home, legacy_page_redirect, projects_hub

urlpatterns = [
    path("", home, name="home"),
    # The former pages remain in the codebase for possible reuse. Public traffic
    # now returns to the relevant section of the single-page commercial site.
    path("sistemas/", legacy_page_redirect, name="systems"),
    path("erp/", legacy_page_redirect, name="erp"),
    path("proyectos/", projects_hub, name="projects_hub"),
    path("desarrollo-web/", legacy_page_redirect, name="web_development_projects"),
    path("catalogo-web/", legacy_page_redirect, name="catalog"),
    path("automatizaciones/", legacy_page_redirect, name="automations"),
]
