# AGENTS.md

Guía para agentes que trabajen en este repositorio.

## Proyecto

- Sitio público de **l-lab.cl**, orientado a pymes chilenas.
- Stack: Python, Django 5.2, plantillas Django, Tailwind CSS mediante CDN y JavaScript nativo.
- Idioma de la interfaz y del contenido: español de Chile.
- La página principal es la única página pública de contenido. Las rutas antiguas se conservan como redirecciones permanentes hacia secciones de la landing.

## Estructura relevante

- `config/settings.py`: configuración general, seguridad, archivos estáticos y entorno.
- `config/urls.py`: rutas globales, sitemap, robots y manejo de errores.
- `portfolio/models.py`: proyectos y consultas de contacto.
- `portfolio/views.py`: contenido y lógica de las vistas; incluye servicios y casos mostrados en la landing.
- `portfolio/forms.py`: formulario de contacto.
- `portfolio/urls.py`: rutas públicas y redirecciones heredadas.
- `portfolio/tests.py`: pruebas de comportamiento público, SEO, redirecciones y contacto.
- `templates/portfolio/home.html`: landing principal y sus scripts/estilos específicos.
- `templates/portfolio/_header.html`: navegación compartida.
- `static/portfolio/`: imágenes, marca, videos y CSS estático.
- `ESTILO_Y_LOGO.md`: fuente de verdad para identidad visual y uso de marca.

## Puesta en marcha

Usar el entorno virtual incluido si está disponible:

```bash
source venv/bin/activate
python manage.py migrate
python manage.py runserver
```

También se pueden ejecutar los comandos directamente con `venv/bin/python`.

Variables relevantes para producción:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_SECURE_HSTS_SECONDS`

No guardar secretos ni tokens en el repositorio. No copiar valores sensibles desde `config/local_settings.py`.

## Validación

Antes de entregar cambios, ejecutar:

```bash
venv/bin/python manage.py check
venv/bin/python manage.py test
```

Si se modifican modelos:

```bash
venv/bin/python manage.py makemigrations --check --dry-run
```

Agregar o actualizar pruebas cuando cambien rutas, contenido crítico, formularios, SEO, recursos estáticos o comportamiento de la landing.

## Reglas funcionales

- Mantener `/` como la única página pública de contenido salvo que el requerimiento indique explícitamente lo contrario.
- Mantener las rutas heredadas como redirecciones `301` hacia `/#soluciones` o `/#casos`.
- Conservar los anclajes principales: `#soluciones`, `#casos`, `#proceso` y `#contacto`.
- El formulario válido abre WhatsApp con el mensaje preparado; no cambiar ese flujo sin confirmación.
- Mantener canonical, metadatos sociales, sitemap, `robots.txt` y la página 404 coherentes con producción.
- No depender de registros concretos de la base SQLite para renderizar contenido esencial.

## Diseño y contenido

- Consultar `ESTILO_Y_LOGO.md` antes de modificar la interfaz.
- Respetar la identidad dark-first: Graphite `#171717`, Smoke `#F4F1EC` y Ember `#FF6A2A`.
- Usar IBM Plex Mono para títulos y etiquetas técnicas; DM Sans para texto corrido.
- Mantener el estilo de laboratorio tecnológico/terminal, bordes sutiles, radios amplios y movimiento contenido.
- Evitar componentes genéricos de plantilla SaaS, gradientes excesivos o nuevos colores protagonistas.
- Toda interfaz nueva debe funcionar en tema oscuro y claro, móvil y escritorio.
- Mantener foco visible y respetar `prefers-reduced-motion`.
- Escribir textos claros, concretos y orientados a problemas reales de pymes; evitar jerga innecesaria.
- Optimizar imágenes y añadir `alt`, `loading="lazy"` y dimensiones cuando corresponda.

## Convenciones de implementación

- Seguir el estilo existente de Django y PEP 8.
- Preferir plantillas Django y JavaScript nativo; no añadir frameworks o dependencias sin necesidad clara.
- La landing usa Tailwind por CDN y algunos estilos en línea en `home.html`; seguir el patrón existente para cambios pequeños.
- Usar `{% static %}` para recursos locales y no enlazar archivos directamente desde `media/`.
- Si un cambio requiere contenido administrable, usar modelos, migraciones y Django Admin en lugar de fijarlo en la plantilla.
- No editar migraciones ya aplicadas; crear una nueva.
- No modificar `db.sqlite3`, archivos generados, cachés `__pycache__` ni `staticfiles/` como parte de una funcionalidad.

## Cuidado con el estado del repositorio

Puede haber cambios locales del usuario. Antes de editar:

```bash
git status --short
git diff -- <archivo>
```

No descartar, revertir ni sobrescribir cambios ajenos. Limitar cada tarea a los archivos necesarios y revisar el diff final antes de responder.
