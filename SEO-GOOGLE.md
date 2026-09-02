# Conectar el sitio con Google — Estudio Jurídico Abog. Blas Santander

El sitio es **una sola landing** (`index.html`), fiel al diseño de Claude Design.
Todo lo técnico ya está hecho. Quedan cuatro trámites en las cuentas de Google y
**dos valores para pegar** en `tools/build.py`.

URL de publicación actual: `https://asbitpy.github.io/Estudio-juridico-Blas-Santander/`
(si cambia, editar `BASE` en `tools/build.py` y regenerar).

---

## Paso 1 · Google Search Console (indexación)

1. Entrar a <https://search.google.com/search-console> con la cuenta del estudio.
2. Agregar propiedad → **Prefijo de URL** → pegar la URL del sitio.
3. Elegir **Etiqueta HTML**. Google muestra algo así:
   `<meta name="google-site-verification" content="AbC123..." />`
4. Copiar **sólo** el valor de `content` y pegarlo en `tools/build.py`:

   ```python
   GSC_TOKEN = "AbC123..."
   ```

5. Regenerar y publicar:

```bash
python tools/build.py
```

6. Volver a Search Console → **Verificar**.
7. En **Sitemaps**, enviar: `sitemap.xml`
8. En **Inspección de URL**, pedir indexación de la portada.

---

## Paso 2 · Google Analytics 4 (medir visitas y consultas)

1. <https://analytics.google.com> → Administrar → **Crear propiedad**.
2. Crear un flujo de datos **Web** con la URL del sitio.
3. Copiar el **ID de medición** (`G-XXXXXXXXXX`) y pegarlo en `tools/build.py`:

   ```python
   GA4_ID = "G-1A2B3C4D5E"
   ```

4. Regenerar (`python tools/build.py`) y publicar.

Mientras el valor tenga `XXXX`, el script de Google **no se carga**: el sitio no
manda datos ni suma peso. Al reemplazarlo se activa solo.

### Conversiones ya instrumentadas

Cada clic a WhatsApp dispara el evento `contacto_whatsapp`:

| Parámetro   | Valor                                                                    |
|-------------|--------------------------------------------------------------------------|
| `ubicacion` | `hero`, `cabecera`, `menu`, `fija`, `contacto`, `contacto-btn`, `pie`, `area-1`…`area-10` |
| `pagina`    | título de la página                                                       |

Los `area-N` permiten ver **qué área legal genera más consultas** — dato directo
para decidir en qué enfocar contenido y publicidad.

Los dos botones de la sección Reseñas disparan sus propios eventos:
`resena_escribir` (fue a dejar una) y `resena_ver` (fue a leerlas). Los enlaces
al mapa reportan `como_llegar` y `como_llegar_dato`.

En GA4 → **Administrar → Eventos**, marcar `contacto_whatsapp` y
`resena_escribir` como **eventos clave (conversión)**.

---

## Paso 3 · Perfil de Empresa en Google (lo más importante en SEO local)

Es lo que hace aparecer al estudio en el mapa cuando alguien busca
"abogado en San Lorenzo".

1. <https://business.google.com> → reclamar o crear el perfil.
2. Datos **idénticos** a los del sitio (Google los cruza):
   - Nombre: `Estudio Jurídico Abog. Blas Santander`
   - Categoría principal: **Abogado**; secundarias: Abogado laboralista,
     Abogado de familia, Abogado penalista, Abogado de bienes raíces
   - Zona de servicio: San Lorenzo y Departamento Central
   - Teléfono: `0984 750 151`
   - Horario: lunes a sábados, 07:00 a 17:00
   - Sitio web: la URL del sitio
3. Cargar el logo y fotos reales del estudio.
4. Pedir reseñas a clientes: es la palanca que más mueve el ranking local.

La dirección ya está publicada y coincide con la del perfil:
`Av. Moisés Bertoni y, San Lorenzo 111459`. El `schema.org` incluye también las
coordenadas (`-25.3805, -57.525071`) y `hasMap` apuntando al enlace de Maps.

### Sección de reseñas en el sitio

La landing tiene una sección **Reseñas** con dos botones:

| Botón | A dónde va |
|---|---|
| Dejar una reseña | `https://g.page/r/CT8mIA5livakEBM/review` — abre el formulario de Google |
| Ver reseñas en Google | ficha del negocio vía Place ID `ChIJX1cKkdKxi0QRPyYgDmWK9qQ` |

El link corto del perfil también quedó en el `sameAs` del `schema.org`, que es
lo que le dice a Google que este sitio y ese Perfil de Empresa son el mismo
negocio. Los dos botones reportan a GA4 como `resena_escribir` y `resena_ver`,
así se puede ver cuánta gente efectivamente va a dejar una reseña.

**Cómo aprovecharla:** mandar el link `https://g.page/r/CT8mIA5livakEBM/review`
por WhatsApp al cerrar cada caso. Es el mismo que usa el botón, y abre el
formulario directo, sin pasos intermedios.

### Reseñas publicadas en el sitio

La sección **Reseñas** muestra las 2 opiniones reales del Perfil de Empresa, con
el texto transcrito literal, el nombre de cada autor y la respuesta del estudio.
El `schema.org` declara `aggregateRating` 5,0 con 2 opiniones y los dos objetos
`Review`, lo que habilita las estrellas en los resultados de Google.

> **Al aparecer una reseña nueva hay que actualizar `tools/build.py`.** Están en
> la lista `RESENAS`, junto con `RESENAS_PROMEDIO` y `RESENAS_TOTAL`. Si los
> números no coinciden con los del Perfil de Empresa, Google puede quitar las
> estrellas del resultado. Conviene revisarlo cada par de meses.

### Unificar el nombre (pendiente en Google)

El nombre oficial es **Estudio Jurídico Abog. Blas Santander**, sin "Edgar".
Así está en todo el sitio y en el `schema.org`.

En el Perfil de Empresa todavía figura como
`Estudio Juridico Abog. Blas Santander-servicios legales`. Hay que editarlo en
<https://business.google.com> y dejarlo exactamente igual al del sitio: Google
cruza nombre, teléfono y dirección entre las dos fuentes, y las diferencias le
restan confianza al perfil.

Mientras tanto, el `schema.org` declara las dos formas en `alternateName`, así
que Google puede reconocerlas como el mismo negocio. Una vez cambiado el
perfil, se puede sacar esa variante de `jsonld_negocio()` en `tools/build.py`.

---

## Paso 4 · Verificar

- Datos estructurados: <https://search.google.com/test/rich-results>
- Velocidad y Core Web Vitals: <https://pagespeed.web.dev>

---

## Lo que ya viene resuelto en el código

| Elemento | Dónde |
|---|---|
| `title` y `meta description` optimizados para "abogado en San Lorenzo" | `landing()` |
| Canonical, `hreflang` es-PY y x-default | `head()` |
| Open Graph + Twitter Card | `head()` |
| `Attorney` con horario, zona de servicio, idiomas (es/gn) y las 10 áreas como `OfferCatalog` | `jsonld_negocio()` |
| `FAQPage` con las 5 preguntas | `jsonld_faq()` |
| `WebSite` | `JSONLD_SITIO` |
| `sitemap.xml` con `lastmod` automático + `robots.txt` | `SITEMAP` / `ROBOTS` |
| Un solo `<h1>`, jerarquía H2/H3 correcta | plantilla |
| `alt` en todas las imágenes, decorativas con `alt=""` | plantilla |
| Imágenes redimensionadas, `srcset` y `loading="lazy"` | `assets/img/` |
| Precarga del hero con `fetchpriority="high"` | `head(precarga_hero=True)` |
| `site.webmanifest` e íconos 180/192/512 | raíz y `assets/img/` |
| 404 con `noindex, follow` | `pagina_404()` |
| `prefers-reduced-motion` respetado | `assets/css/style.css` |
| Dirección, `geo` y `hasMap` en el `schema.org` | `jsonld_negocio()` |
| `aggregateRating` + `Review` con las opiniones reales | lista `RESENAS` |
| 20 zonas del Central declaradas en `areaServed` y visibles en la página | lista `ZONAS` |
| Dirección enlazada a Google Maps y botón **Cómo llegar** en contacto | plantilla |
| `<noscript>` que muestra todo si falla el JavaScript | `head()` |

### Si más adelante quieren subir en Google

Una landing sola compite bien por "abogado en San Lorenzo", pero no por
"abogado laboral San Lorenzo", "usucapión San Lorenzo", etc. Para eso hacen falta
páginas propias por área. La arquitectura ya está preparada: las 10 áreas viven
en la lista `AREAS` de `tools/build.py` y se pueden expandir a páginas
individuales sin rehacer nada.

---

## Regenerar el sitio

Todo el contenido está en `tools/build.py`, marcado por origen:
`[D]` literal del diseño · `[C]` del documento del cliente · `[AS]` redactado por AS BIT.

```bash
python tools/build.py
```

Nunca editar `index.html` a mano: se pisa en la siguiente generación.
