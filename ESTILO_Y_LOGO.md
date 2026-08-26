# Guía estética y de logo — l-lab.cl

Documento de referencia visual para replicar la identidad de esta página en otra interfaz. Describe únicamente la estética, composición, tipografía, color, tratamiento visual y logo; no define funcionalidades ni estructura técnica.

## 1. Dirección visual

- **Concepto:** laboratorio tecnológico / terminal de desarrollo / infraestructura digital.
- **Personalidad:** técnica, precisa, contemporánea, profesional y cercana.
- **Sensación general:** una interfaz de software premium, con atmósfera oscura, detalles de consola y acentos luminosos.
- **Estilo:** dark-first, editorial y modular; combinar superficies sobrias con pequeños elementos de señalización técnica.
- **Evitar:** apariencia corporativa genérica, exceso de gradientes, ilustraciones caricaturescas, colores neón múltiples o estética de plantilla SaaS.
- **Riesgo visual distintivo:** usar una cuadrícula técnica, puntos de conexión y textura de grano como atmósfera, manteniendo el contenido legible y el resto de la composición sobria.

## 2. Paleta cromática

### Colores principales

| Nombre | Hex | Uso |
|---|---:|---|
| Graphite | `#171717` | Fondo principal oscuro, texto sobre fondos claros y botones secundarios. |
| Deep terminal | `#0B0B0B` | Paneles tipo consola o terminal. |
| Smoke | `#F4F1EC` | Texto principal, superficies claras y contraste alto. |
| Ash | `#D8D2C8` | Texto secundario claro, metadatos y detalles apagados. |
| Ember | `#FF6A2A` | Color de marca: botones primarios, enlaces activos, puntos y estados destacados. |
| Copper | `#B64A22` | Variante oscura del naranja para sombras, estados o acentos secundarios. |

### Colores de apoyo

- **Cyan técnico:** `#67E8F9` / `#CFFAFE`. Usarlo de forma puntual para automatización, tecnología avanzada o estados alternativos.
- **Lime:** `#BEF264`. Acento ocasional para destacar una categoría distinta.
- **Fondos de sección:** `#1D1C1A`, `#121110` y, en tema claro, `#E8E2D8` / `#EFE7DC`.
- Los acentos cyan, lime y fucsia son secundarios: el naranja Ember debe seguir siendo el color de marca dominante.

### Reglas de contraste y aplicación

- Priorizar fondo Graphite y texto Smoke.
- Aplicar Ember en pequeñas dosis: aproximadamente para acciones, indicadores y palabras clave, no como fondo general.
- Usar fondos blancos translúcidos sobre oscuro (`rgba(244,241,236,.035–.06)`) para crear tarjetas discretas.
- Usar bordes finos y translúcidos (`rgba(244,241,236,.10–.16)`), nunca bordes gruesos o muy contrastados.
- Los brillos naranjas deben ser suaves y amplios, por ejemplo `0 0 60px rgba(255,106,42,.18)`.

## 3. Tipografía

### Tipografías

- **Display y titulares:** `IBM Plex Mono`, monospace.
- **Texto corrido y controles:** `DM Sans`, sans-serif.
- **Etiquetas técnicas, navegación y datos:** `IBM Plex Mono`.

### Tratamiento tipográfico

- Titulares grandes, en mayúsculas, con peso medio y tracking negativo pronunciado.
- Usar titulares compactos, geométricos y de alto impacto; evitar serifas.
- Texto de lectura en DM Sans, con tamaño cómodo y altura de línea amplia.
- Etiquetas pequeñas en mayúsculas, monoespaciadas, con tracking amplio (`.18em–.45em`) y color Ember.
- Los precios, comandos y datos pueden usar IBM Plex Mono para reforzar la sensación de sistema.
- Jerarquía recomendada: eyebrow técnico pequeño → titular monoespaciado grande → descripción en sans-serif → acción destacada.

## 4. Composición y layout

- Contenedor de contenido amplio y centrado, con ancho máximo aproximado de `1200–1280px`.
- Márgenes laterales generosos en desktop; padding reducido pero consistente en móvil.
- Secciones verticales espaciosas, con aproximadamente `80–100px` de separación.
- Preferir grids de 2 o 3 columnas para tarjetas y módulos.
- Usar una hero dividida: texto principal a la izquierda y panel técnico/terminal a la derecha.
- Las tarjetas tienen esquinas redondeadas grandes, normalmente entre `20px` y `32px`.
- No usar sombras pesadas por defecto; reservarlas para paneles destacados o el brillo del CTA.
- Separar secciones mediante líneas horizontales finas y cambios sutiles de tono en el fondo.
- El diseño debe sentirse aireado, pero no minimalista vacío: las cuadrículas, etiquetas y paneles aportan densidad técnica.

## 5. Fondos y textura

### Cuadrícula técnica

- Añadir una cuadrícula de líneas muy sutiles, horizontales y verticales, aproximadamente cada `72px`.
- Opacidad baja: entre `0.04` y `0.08`.
- En la hero, aplicar una máscara radial para que la cuadrícula se concentre cerca del centro y desaparezca hacia los bordes.
- Incorporar puntos pequeños naranjas y grises alineados a la cuadrícula, como nodos de una red o señales de circuito.

### Textura de grano

- Aplicar una textura de ruido/grano muy sutil sobre toda la página.
- Debe ser fija, no bloquear interacciones y tener una opacidad aproximada de `0.07–0.13`.
- La textura debe sentirse casi fotográfica/industrial, nunca sucia ni dominante.

### Iluminación

- Usar manchas radiales desenfocadas en Ember con opacidad baja, sobre todo en la esquina superior izquierda o alrededor de elementos destacados.
- Mantener el resto del fondo casi negro y plano para que el naranja tenga protagonismo.
- El efecto de iluminación es ambiental, no un gradiente protagonista.

## 6. Componentes visuales

### Navegación

- Barra superior fija o sticky.
- Fondo Graphite semitransparente con `backdrop-blur`.
- Línea inferior fina y translúcida.
- Logo alineado a la izquierda; navegación monoespaciada, pequeña, en mayúsculas y con tracking amplio.
- Enlaces inactivos en Smoke con opacidad reducida; hover y estado activo en Ember.
- Botón de contacto tipo píldora, con borde Ember y relleno Ember al pasar el cursor.

### Botones

- Forma de píldora (`border-radius: 9999px`).
- CTA primario: fondo Ember, texto Graphite, peso fuerte y sombra naranja suave.
- Acción secundaria: transparente, borde blanco translúcido y texto Smoke.
- Hover: leve desplazamiento vertical (`1–2px`), cambio sutil de brillo o relleno, sin animaciones exageradas.

### Tarjetas

- Fondo translúcido claro sobre Graphite.
- Borde de 1px, poco visible.
- Radio grande (`20–26px`).
- Padding generoso.
- Hover con desplazamiento mínimo hacia arriba, borde Ember y brillo suave.
- Las tarjetas deben parecer módulos de una interfaz, no cajas blancas aisladas.

### Panel terminal

- Fondo casi negro (`#0B0B0B`), borde o ring muy sutil y esquinas redondeadas.
- Tipografía IBM Plex Mono pequeña.
- Encabezado con tres puntos tipo ventana: rojo, amarillo y verde.
- Texto claro, comandos en Smoke, prompts o indicadores en Ember.
- Cursor rectangular naranja parpadeante como detalle de vida.

## 7. Logo

### Elemento de marca

El logo gráfico está en `media/logo_l-lab.png` y tiene formato PNG cuadrado de aproximadamente `1254 × 1254 px`, con fondo oscuro y esquinas redondeadas.

### Construcción visual

- **Base:** cuadrado oscuro casi negro, con esquinas muy redondeadas.
- **Marco:** circuito perimetral discontinuo, compuesto por segmentos en gris carbón y Ember.
- **Símbolo central:** prompt de terminal `>_` en Smoke/blanco cálido.
  - El signo `>` es grande, grueso y angular.
  - El guion bajo `_` es horizontal, corto y robusto.
- **Nodos:** círculos naranjas de diferentes tamaños ubicados en intersecciones y extremos del circuito.
- **Fondo interno:** cuadrícula tenue con puntos de conexión, evocando circuitos, nodos y coordenadas.
- **Acabado:** textura granulada y ligeramente industrial; no debe verse completamente plano o excesivamente pulido.
- **Contraste:** símbolo central claro, circuito naranja/gris y fondo Graphite.

### Significado visual

El símbolo combina tres ideas: terminal de programación (`>_`), laboratorio experimental (`lab`) y red de conexiones digitales. La identidad debe conservar esa lectura tecnológica sin convertirse en un ícono genérico de código.

### Uso del logo

- Mantener una zona de seguridad alrededor del logo igual a, al menos, `10%` de su tamaño.
- No deformarlo ni cambiar su proporción cuadrada.
- No girarlo, inclinarlo ni agregarle sombras duras.
- No reemplazar el naranja por otros colores de acento.
- Sobre fondos oscuros funciona en su versión original; sobre fondos claros usar una versión con suficiente contraste, conservando el símbolo y el Ember.
- Para tamaños pequeños, priorizar el isotipo gráfico; el nombre escrito puede funcionar como wordmark independiente.
- En la navegación actual, el nombre se presenta como **`l-lab`** en IBM Plex Mono, con **`cl`** pequeño, en mayúsculas y color Ember.

## 8. Microinteracciones y movimiento

- Animaciones cortas y discretas, con curvas suaves.
- Entrada de contenido: aparecer con opacidad y desplazamiento vertical de aproximadamente `18px`.
- Hover de tarjetas y botones: elevación mínima, cambio de borde y brillo.
- La cuadrícula/puntos de la hero pueden desplazarse lentamente como una señal de red.
- El cursor de terminal puede parpadear.
- Respetar `prefers-reduced-motion`: desactivar movimiento ambiental y dejar solo transiciones esenciales.

## 9. Tema claro opcional

La identidad también admite un modo claro:

- Fondo principal: Smoke (`#F4F1EC`).
- Texto principal: Graphite (`#171717`).
- Secciones: beige/gris cálido (`#E8E2D8`, `#EFE7DC`).
- Conservar Ember como acento.
- Invertir bordes, cuadrículas y transparencias para usar negro con opacidad baja.
- Mantener los paneles terminal en oscuro para conservar el contraste y la personalidad técnica.

## 10. Resumen para otra IA

> Diseña una interfaz dark-first para un estudio tecnológico llamado l-lab. Usa Graphite casi negro, texto Smoke cálido y Ember naranja como acento principal. Combina IBM Plex Mono para titulares, etiquetas y datos con DM Sans para lectura. La estética debe recordar un laboratorio de software y una terminal: cuadrícula técnica sutil, nodos naranjas, grano ambiental, paneles translúcidos, bordes finos, radios grandes y CTAs en forma de píldora. El logo es un cuadrado oscuro de esquinas redondeadas con un prompt `>_` blanco al centro, rodeado por un circuito perimetral discontinuo naranja/gris, nodos naranjas y una cuadrícula tenue. Mantén la composición elegante, aireada y profesional; los detalles técnicos deben ser acentos, no ruido visual.
