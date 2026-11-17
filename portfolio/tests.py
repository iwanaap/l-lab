from urllib.parse import parse_qs, urlparse

from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(SECURE_SSL_REDIRECT=False)
class PublicLandingPageTests(TestCase):
    def test_home_is_the_only_public_content_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/home.html")
        self.assertContains(response, 'rel="canonical" href="https://l-lab.cl/"')

    def test_legacy_pages_redirect_to_landing_sections(self):
        destinations = {
            "systems": "/#soluciones",
            "erp": "/#soluciones",
            "web_development_projects": "/#casos",
            "catalog": "/#soluciones",
            "automations": "/#soluciones",
            "projects_hub": "/#casos",
        }
        for name, destination in destinations.items():
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 301)
                self.assertEqual(response["Location"], destination)

    def test_landing_has_clear_conversion_structure(self):
        response = self.client.get(reverse("home"))
        for copy in (
            "l-lab <span>ordena tu negocio.</span>",
            "Consigue más consultas",
            "Centraliza tu operación",
            "Deja de repetir tareas",
            "Soluciones que ya están funcionando.",
            "Cuéntame qué quieres mejorar.",
            "Enviar consulta por WhatsApp",
        ):
            self.assertContains(response, copy)
        self.assertEqual(len(response.context["services"]), 3)
        self.assertEqual(len(response.context["case_studies"]), 2)

    def test_hero_prioritizes_websites_and_has_accessible_scene(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()
        hero = content.split('<main id="inicio">', 1)[1].split('</section>', 1)[0]
        self.assertIn("Páginas web para pymes", hero)
        self.assertIn("l-lab <span>ordena tu negocio.</span>", hero)
        self.assertLess(hero.index('id="web-build"'), hero.index('<h1'))
        self.assertIn('href="#contacto"', hero)
        self.assertIn("Hablemos de tu web", hero)
        self.assertIn('href="#casos"', hero)
        self.assertIn("Ver proyectos", hero)
        self.assertIn("sistemas ERP y automatizaciones", hero)
        self.assertIn('aria-label="Demostración:', hero)
        for removed_copy in (
            "De piezas sueltas a tu propia web",
            "Diseño + contenido + contacto. Todo en su lugar.",
            "Lo que hace único a tu negocio, en una web que lo conecta.",
            "Una presencia clara. Un próximo paso fácil.",
        ):
            self.assertNotIn(removed_copy, hero)
        self.assertNotIn('id="web-build-status"', hero)
        self.assertIn('id="web-build-replay" hidden', hero)
        self.assertNotIn('id="terminal-output"', content)
        self.assertNotIn('id="typing-title"', content)
        self.assertContains(response, '/static/portfolio/hero.css')
        self.assertContains(response, '/static/portfolio/hero.js')

    def test_footer_has_direct_contact_and_project_links(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "portfolio/_footer.html")
        footer = response.content.decode().split('<footer', 1)[1].split('</footer>', 1)[0]
        self.assertIn('href="tel:+56934821394"', footer)
        self.assertIn("+56 9 3482 1394", footer)
        self.assertIn('href="https://wa.me/56934821394"', footer)
        self.assertIn('href="#contacto"', footer)
        self.assertIn('href="#inicio"', footer)
        self.assertIn('aria-labelledby="footer-projects-title"', footer)
        self.assertNotIn("↗", footer)
        self.assertNotIn("↑", footer)
        self.assertIn('class="site-footer-cta"', footer)
        self.assertIn('class="site-footer-link"', footer)
        for project_url in (
            "https://neuquemas.l-lab.cl",
            "https://erp.l-lab.cl",
        ):
            self.assertIn(
                f'href="{project_url}" target="_blank" rel="noopener noreferrer"',
                footer,
            )
        self.assertContains(response, '/static/portfolio/css/footer.css')

    def test_prices_and_links_to_old_pages_are_not_rendered(self):
        content = self.client.get(reverse("home")).content.decode()
        self.assertNotIn('id="precios"', content)
        self.assertNotIn(">Precios<", content)
        for old_path in (
            "/desarrollo-web/",
            "/catalogo-web/",
            "/erp/",
            "/automatizaciones/",
            "/sistemas/",
        ):
            self.assertNotIn(f'href="{old_path}"', content)

    def test_navigation_only_uses_landing_sections(self):
        response = self.client.get(reverse("home"))
        header = response.content.decode().split("<header", 1)[1].split("</header>", 1)[0]
        for anchor in ("/#soluciones", "/#casos", "/#proceso", "/#contacto"):
            self.assertIn(f'href="{anchor}"', header)
        self.assertNotIn("Precios", header)
        self.assertNotIn("Automatizaciones</a>", header)
        self.assertNotIn("Desarrollo web</a>", header)

    def test_contact_opens_whatsapp_with_submitted_details(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Ana Pérez",
                "phone": "+56 9 1111 2222",
                "service": "Ordenar mi operación",
                "message": "Necesito centralizar las cotizaciones.",
            },
        )
        self.assertEqual(response.status_code, 302)
        redirect_url = urlparse(response["Location"])
        self.assertEqual(redirect_url.netloc, "wa.me")
        self.assertEqual(redirect_url.path, "/56934821394")
        whatsapp_text = parse_qs(redirect_url.query)["text"][0]
        self.assertIn("Ana Pérez", whatsapp_text)
        self.assertIn("Ordenar mi operación", whatsapp_text)
        self.assertIn("Necesito centralizar las cotizaciones.", whatsapp_text)

    def test_invalid_contact_submission_shows_errors(self):
        response = self.client.post(reverse("home"), {"name": "", "service": "", "message": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Revisa los campos del formulario")
        self.assertContains(response, "Este campo es obligatorio")

    def test_sitemap_only_contains_home(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<loc>https://testserver/</loc>", html=True)
        for path in ("desarrollo-web", "catalogo-web", "erp/", "automatizaciones", "sistemas/"):
            self.assertNotContains(response, path)

    def test_robots_points_to_sitemap_and_blocks_admin(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "https://l-lab.cl/sitemap.xml")

    @override_settings(DEBUG=False)
    def test_custom_404_hides_framework_details(self):
        response = self.client.get("/ruta-que-no-existe/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Esta página no existe", status_code=404)

    def test_static_assets_used_by_landing_are_available(self):
        for asset in (
            "/static/portfolio/css/footer.css",
            "/static/portfolio/hero.css",
            "/static/portfolio/hero.js",
            "/static/portfolio/images/hero-negocio.svg",
            "/static/portfolio/brand/logo-l-lab.png",
            "/static/portfolio/images/adp-seguridad.png",
            "/static/portfolio/images/renmai-ficha-clinica.png",
            "/static/portfolio/images/nelson-landaeta.jpg",
        ):
            with self.subTest(asset=asset):
                self.assertEqual(self.client.get(asset).status_code, 200)
