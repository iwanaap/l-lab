from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Project


@override_settings(SECURE_SSL_REDIRECT=False)
class PublicSiteTests(TestCase):
    def test_commercial_pages_are_available(self):
        for name in (
            "home",
            "web_development_projects",
            "catalog",
            "erp",
            "automations",
            "systems",
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'rel="canonical"')

    def test_robots_points_to_sitemap_and_blocks_admin(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "https://l-lab.cl/sitemap.xml")

    def test_sitemap_contains_public_routes(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        for path in ("/", "/desarrollo-web/", "/catalogo-web/", "/erp/", "/automatizaciones/", "/sistemas/"):
            self.assertContains(response, path)

    @override_settings(DEBUG=False)
    def test_custom_404_hides_framework_details(self):
        response = self.client.get("/ruta-que-no-existe/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Esta página no existe", status_code=404)
        self.assertNotContains(response, "URLconf", status_code=404)

    def test_home_has_conversion_message_and_structured_data(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Agenda un diagnóstico")
        self.assertContains(response, "Problemas reales. Soluciones concretas.")
        self.assertContains(response, "Cómo trabajamos")
        self.assertContains(response, 'application/ld+json')

    def test_service_pages_use_concrete_commercial_copy(self):
        catalog = self.client.get(reverse("catalog"))
        self.assertContains(catalog, "Ferreterías")
        self.assertContains(catalog, "Ventas por WhatsApp")

        erp = self.client.get(reverse("erp"))
        self.assertContains(erp, "Tu operación, bajo control")
        self.assertContains(erp, "Inventario por bodega y variante")
        self.assertContains(erp, "Multiempresa, permisos y auditoría")
        self.assertContains(erp, "Dashboard general")
        self.assertContains(erp, "/static/portfolio/images/erp-login.png")
        self.assertContains(erp, "/static/portfolio/images/erp-dashboard.png")
        self.assertNotContains(erp, "Ejemplos de interfaz")

        automations = self.client.get(reverse("automations"))
        self.assertContains(automations, "Formulario a lead y seguimiento")
        self.assertContains(automations, "Aviso de tareas vencidas")

        systems = self.client.get(reverse("systems"))
        self.assertContains(systems, "ERP Empresas")
        self.assertContains(systems, "Aula Virtual")
        self.assertContains(systems, "No partimos de cero")

    def test_main_service_pages_share_the_primary_cta(self):
        cta = "Agenda un diagnóstico"
        for name in ("home", "web_development_projects", "catalog", "erp", "automations", "systems"):
            with self.subTest(name=name):
                self.assertContains(self.client.get(reverse(name)), cta)

    def test_all_pages_use_the_same_navigation(self):
        links = (
            "Inicio",
            "Soluciones",
            "Automatizaciones",
            "Desarrollo web",
            "Sistemas",
            "Casos",
            "Nosotros",
            "Precios",
            "Contacto",
        )
        for name in ("home", "web_development_projects", "catalog", "erp", "automations", "systems"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertTemplateUsed(response, "portfolio/_header.html")
                for link in links:
                    self.assertContains(response, link)
                self.assertContains(response, 'href="/#nosotros"')
                header = response.content.decode().split("<header", 1)[1].split("</header>", 1)[0]
                self.assertLess(header.index("Automatizaciones"), header.index("Desarrollo web"))
                self.assertLess(header.index("Desarrollo web"), header.index("Sistemas"))
                self.assertNotIn('href="/catalogo-web/"', header)
                self.assertNotIn('href="/erp/"', header)

    def test_home_is_a_concise_commercial_guide(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["services"]), 4)
        self.assertEqual(len(response.context["case_studies"]), 3)
        for removed_copy in (
            "Problemas que resolvemos",
            "Menos fricción para vender y operar",
            "No llegan suficientes consultas",
            "Tu catálogo vive en WhatsApp",
            "Tu operación depende de Excel",
            "Pierdes tiempo en tareas repetidas",
        ):
            self.assertNotContains(response, removed_copy)
        self.assertContains(response, "Web profesional")
        self.assertContains(response, "Ordenamos tus operaciones")
        self.assertContains(response, "Sistemas para tu negocio")
        self.assertContains(response, 'href="/sistemas/"', count=4)
        self.assertContains(response, "Valores base.")
        self.assertContains(response, "Proyectos completos se cotizan según alcance.")
        self.assertContains(response, "Trabajo humano")
        self.assertContains(response, "Full-Stack Developer")
        self.assertContains(response, "nelson-landaeta.jpg")
        self.assertContains(response, "linkedin.com/in/nelson-ignacio-landaeta-toro/")
        self.assertContains(response, "Soy Nelson.")
        self.assertNotContains(response, "Repositorio comercial")
        self.assertNotContains(response, "Misión")
        self.assertNotContains(response, "Solitario")

    def test_favicon_is_available_on_every_page(self):
        favicon_url = "/static/portfolio/brand/logo-l-lab.png"
        for name in ("home", "web_development_projects", "catalog", "erp", "automations", "systems"):
            with self.subTest(name=name):
                self.assertContains(self.client.get(reverse(name)), favicon_url)

        redirect_response = self.client.get("/favicon.ico")
        self.assertRedirects(
            redirect_response,
            favicon_url,
            status_code=301,
            fetch_redirect_response=False,
        )
        asset_response = self.client.get(favicon_url)
        self.assertEqual(asset_response.status_code, 200)
        self.assertEqual(asset_response["Content-Type"], "image/png")

    def test_case_study_images_use_deployable_static_assets(self):
        response = self.client.get(reverse("home"))
        for image in (
            "/static/portfolio/images/adp-seguridad.png",
            "/static/portfolio/images/renmai-ficha-clinica.png",
            "/static/portfolio/images/likan-propiedades.png",
        ):
            self.assertContains(response, image)
            asset_response = self.client.get(image)
            self.assertEqual(asset_response.status_code, 200)

    def test_erp_uses_real_deployable_interface_images(self):
        response = self.client.get(reverse("erp"))
        for image in (
            "/static/portfolio/images/erp-login.png",
            "/static/portfolio/images/erp-dashboard.png",
        ):
            self.assertContains(response, image)
            asset_response = self.client.get(image)
            self.assertEqual(asset_response.status_code, 200)
            self.assertEqual(asset_response["Content-Type"], "image/png")

    def test_solitario_is_separated_as_a_lab_project(self):
        Project.objects.create(
            title="Solitario",
            short_description="Experimento interactivo",
            status="published",
        )
        response = self.client.get(reverse("web_development_projects"))
        self.assertContains(response, "Laboratorio")
        self.assertContains(response, "Experimento / no comercial")
        self.assertContains(response, "Solitario")
        self.assertContains(response, "/static/portfolio/videos/solitario.mp4")
