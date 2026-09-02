# Estudio Jurídico Abog. Blas Santander

Sitio web del estudio jurídico de Blas Santander, en San Lorenzo, Departamento
Central, Paraguay.

**Publicado en:** https://asbitpy.github.io/Estudio-juridico-Blas-Santander/

---

## Cómo está armado

Es una landing estática, sin dependencias ni framework: HTML, CSS y JavaScript
plano. Pesa unos 300 KB en la primera carga.

```
index.html            generado — no editar a mano
404.html              generado — no editar a mano
sitemap.xml           generado
robots.txt            generado
site.webmanifest      generado
assets/css/style.css  sistema visual (Manual de Marca BS)
assets/js/main.js     interacciones y animaciones
assets/img/           imágenes optimizadas para web
tools/build.py        TODO el contenido vive acá
SEO-GOOGLE.md         cómo conectar el sitio con Google
```

## Regenerar el sitio

Cualquier cambio de texto, área, reseña o pregunta frecuente se hace en
`tools/build.py` y después:

```bash
python tools/build.py
```

Eso reescribe los HTML, el sitemap, el robots y el manifest.
**Nunca editar `index.html` a mano:** se pisa en la siguiente generación.

## Marca

Del Manual de Marca BS:

| Color | Hex | Uso |
|---|---|---|
| Negro | `#0E0F12` | fondo principal |
| Carbón | `#1B1D21` | superficies y tarjetas |
| Marfil | `#F2EDE3` | fondos claros |
| Oro | `#C9A24A` | acentos |

Tipografías: **Marcellus** (títulos) + **Nunito Sans** (texto).

## Origen del contenido

Cada texto en `tools/build.py` está marcado con su procedencia:

- `[D]` copiado literal del diseño aprobado
- `[C]` tomado del documento del cliente
- `[AS]` redactado por AS BIT — a revisar con el cliente

Las reseñas de la sección **Reseñas** son las publicadas en el Perfil de Empresa
en Google, transcritas literalmente. Al aparecer una nueva hay que actualizar la
lista `RESENAS` junto con `RESENAS_PROMEDIO` y `RESENAS_TOTAL`.

## Pendiente

- Pegar el ID de Google Analytics 4 y el token de Search Console en
  `tools/build.py` (ver [SEO-GOOGLE.md](SEO-GOOGLE.md))
- Imagen 1200×630 para la vista previa al compartir por WhatsApp

---

Web desarrollada por [AS BIT](https://asbit.com.py).
