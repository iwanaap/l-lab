"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import RedirectView

from portfolio.sitemaps import StaticViewSitemap


def robots_txt(request):
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: https://l-lab.cl/sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")


sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(url='/static/portfolio/brand/logo-l-lab.png', permanent=True),
        name='favicon',
    ),
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('portfolio.urls')),
]

handler404 = "portfolio.views.custom_404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
