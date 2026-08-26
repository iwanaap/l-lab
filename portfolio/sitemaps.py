from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Public commercial pages included in the XML sitemap."""

    protocol = "https"
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            "home",
            "web_development_projects",
            "catalog",
            "erp",
            "automations",
            "systems",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.8
