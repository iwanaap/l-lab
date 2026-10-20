from urllib.parse import parse_qs, urlparse

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

    def test_contact_uses_whatsapp_without_exposing_an_email_address(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Continuar en WhatsApp")
        self.assertContains(response, "WhatsApp +56 9 3482 1394")
        self.assertNotContains(response, "contacto@l-lab.cl")
        self.assertNotContains(response, 'type="email"')
        self.assertNotContains(response, "mailto:")

        response = self.client.post(
            reverse("home"),
            {
                "name": "Ana Pérez",
                "phone": "+56 9 1111 2222",
                "service": "Web profesional",
                "message": "Necesito renovar mi sitio.",
            },
        )
        self.assertEqual(response.status_code, 302)
        redirect_url = urlparse(response["Location"])
        self.assertEqual(redirect_url.netloc, "wa.me")
        self.assertEqual(redirect_url.path, "/56934821394")
        whatsapp_text = parse_qs(redirect_url.query)["text"][0]
        self.assertIn("Ana Pérez", whatsapp_text)
        self.assertIn("Web profesional", whatsapp_text)
        self.assertIn("Necesito renovar mi sitio.", whatsapp_text)
        self.assertNotIn("Email", whatsapp_text)

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
        self.assertContains(systems, "Elige el sistema")
        self.assertContains(systems, "que se acerca a lo que necesitas.")
        self.assertNotContains(systems, "Sistemas disponibles")
        self.assertNotContains(systems, "No partimos de cero")
        self.assertNotContains(systems, "Tenemos sistemas construidos")
        self.assertNotContains(systems, "SYS—01")
        self.assertNotContains(systems, "SYS—02")
        self.assertNotContains(systems, ">60%</span>")

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

    def test_flag_garland_is_not_rendered(self):
        for name in ("home", "web_development_projects", "catalog", "erp", "automations", "systems"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertNotContains(response, "/static/portfolio/css/fiestas-patrias.css")
                self.assertNotContains(response, 'class="guirnalda-chilena"')

    def test_home_is_a_concise_commercial_guide(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["services"]), 4)
        self.assertEqual(len(response.context["case_studies"]), 2)
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
        ):
            self.assertContains(response, image)
            asset_response = self.client.get(image)
            self.assertEqual(asset_response.status_code, 200)

    def test_case_studies_link_to_live_projects(self):
        response = self.client.get(reverse("home"))
        for project_url in (
            "https://adpseguridad.cl",
            "https://fichaclinica.renmai.cl",
        ):
            self.assertContains(response, f'href="{project_url}"')
        self.assertContains(response, "Visitar proyecto", count=2)
        self.assertNotContains(response, "Ver una solución similar")

    def test_likan_propiedades_is_hidden_from_home_and_web_development(self):
        Project.objects.update_or_create(
            slug="likan-propiedades",
            defaults={
                "title": "Likan Propiedades",
                "short_description": "Catálogo inmobiliario",
                "project_url": "https://www.likanpropiedades.cl",
                "status": "published",
            },
        )
        for name in ("home", "web_development_projects"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertNotContains(response, "Likan Propiedades")
                self.assertNotContains(response, "likanpropiedades.cl")

    def test_encaminar_replaces_abordar_on_web_development_page(self):
        response = self.client.get(reverse("web_development_projects"))
        image_url = "/static/portfolio/images/encaminar.png"
        self.assertContains(response, "Encaminar")
        self.assertContains(response, "https://encaminar.cl")
        self.assertContains(response, "Django")
        self.assertContains(response, "Tailwind")
        self.assertContains(response, image_url)
        self.assertNotContains(response, "Abordar")
        self.assertEqual(self.client.get(image_url).status_code, 200)

    def test_renmai_uses_its_deployable_preview_on_web_development_page(self):
        Project.objects.create(
            title="Renmai",
            short_description="Sitio web de Renmai",
            project_url="https://renmai.cl",
            status="published",
        )
        response = self.client.get(reverse("web_development_projects"))
        image_url = "/static/portfolio/images/renmai.png"
        self.assertContains(response, image_url)
        self.assertEqual(self.client.get(image_url).status_code, 200)

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
