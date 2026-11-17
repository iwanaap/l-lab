from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """The public commercial site is intentionally a single landing page."""

    protocol = "https"
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)
