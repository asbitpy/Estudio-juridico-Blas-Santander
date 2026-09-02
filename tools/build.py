# -*- coding: utf-8 -*-
"""
Generador del sitio del Estudio Jurídico Abog. Blas Santander.

    python tools/build.py

Escribe index.html, 404.html, sitemap.xml, robots.txt y site.webmanifest.

FUENTES DE CONTENIDO (únicas):
  · el diseño "Web Abogado Santander.dc.html" de Claude Design
  · el documento del cliente "ESTUDIO JURIDICO ABOG.. BLAS EDGAR.md"

Cada texto está marcado con su origen:
  [D]  copiado literal del diseño
  [C]  tomado del documento del cliente
  [AS] redactado por AS BIT en la voz del diseño — a revisar con el cliente
"""

import io
import os
from datetime import date
from urllib.parse import quote

# ------------------------------------------------------------------ datos

BASE = "https://asbitpy.github.io/Estudio-juridico-Blas-Santander/"

# [C] documento del cliente
TEL_LINDO = "0984 750 151"
TEL_E164 = "+595984750151"
WA = "595984750151"
CIUDAD = "San Lorenzo"
REGION = "Departamento Central"
HORARIO = "Lunes a sábados, de 7:00 a 17:00"
HORARIO_ABRE = "07:00"
HORARIO_CIERRA = "17:00"
IG = "https://www.instagram.com/blassantander9/"
TIKTOK = "https://www.tiktok.com/@blas.santander7"

# Perfil de Empresa en Google (link corto que pasó el cliente).
# El Place ID sale de seguir la redirección de ese link corto.
GOOGLE_PERFIL = "https://g.page/r/CT8mIA5livakEBM"
GOOGLE_RESENA = "https://g.page/r/CT8mIA5livakEBM/review"
GOOGLE_PLACE_ID = "ChIJX1cKkdKxi0QRPyYgDmWK9qQ"
GOOGLE_VER_RESENAS = "https://search.google.com/local/reviews?placeid=" + GOOGLE_PLACE_ID
GOOGLE_MAPA = "https://maps.app.goo.gl/B9xK4WuVq4MHmPoH9"

# [C] dirección del estudio
DIRECCION = "Av. Moisés Bertoni y, San Lorenzo 111459"
CALLE = "Av. Moisés Bertoni y"
CP = "111459"

# Reseñas publicadas en el Perfil de Empresa. Verificadas el 2026-09-01:
# 2 opiniones, ambas de 5 estrellas. Texto transcrito literal de Google.
# Al cambiar esto hay que actualizar también RESENAS_PROMEDIO y RESENAS_TOTAL.
RESENAS_PROMEDIO = "5.0"
RESENAS_TOTAL = "2"
RESENAS = [
    ("Lucas Leguizamón", 5,
     "Gracias por ayudarme en los casos judiciales, hubo buen acompañamiento desde principio al fin, EXCELENTE",
     "muchas gracias, estamos a disposición"),
    ("Alejandro José Santander Gómez", 5,
     "Buen servicio de abogado",
     None),
]

# Distritos del Departamento Central donde el estudio presta servicio.
ZONAS = [
    "San Lorenzo", "Fernando de la Mora", "Capiatá", "Luque", "Ñemby",
    "Lambaré", "San Antonio", "Villa Elisa", "Mariano Roque Alonso", "Limpio",
    "Itauguá", "Areguá", "Ypacaraí", "Ypané", "Guarambaré", "Itá",
    "J. Augusto Saldívar", "Villeta", "Nueva Italia", "Asunción",
]

# Reemplazar cuando existan las cuentas (ver SEO-GOOGLE.md).
GA4_ID = "G-XXXXXXXXXX"
GSC_TOKEN = "PEGAR-TOKEN-SEARCH-CONSOLE"


def wa_link(mensaje):
    return "https://wa.me/%s?text=%s" % (WA, quote(mensaje))


WA_GENERAL = wa_link("Hola, quisiera hacer una consulta legal.")

# ------------------------------------------------------------------ iconos

I = {
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.2-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-.3-.1-1.2-.4-2.3-1.4-.8-.7-1.4-1.6-1.6-1.9-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.1.2-.3.3-.4.1-.2 0-.4 0-.5-.1-.2-.6-1.4-.8-1.9-.2-.4-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9 1-.9 2.3 0 1.4 1 2.7 1.1 2.9.1.2 2 3 4.8 4.2.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.6 1.4 5.1L2 22l5-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.5-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.5 13.5 3.5 12c0-4.7 3.8-8.5 8.5-8.5s8.5 3.8 8.5 8.5-3.8 8.5-8.5 8.5z"/></svg>',
    "flecha": '<svg class="flecha" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" width="15" height="15"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "mapa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "reloj": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 14"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 1.9.6 2.8a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.5 2.8.6a2 2 0 0 1 1.7 2z"/></svg>',
    "maletin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "familia": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17.5" cy="9.5" r="2.2"/><path d="M15 20a5 5 0 0 1 6.5-4.3"/></svg>',
    "balanza": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v18M7 21h10M4 7h16M4 7l-2.2 5.6a3 3 0 0 0 4.4 0zM20 7l2.2 5.6a3 3 0 0 1-4.4 0z"/><path d="M12 3 4 7M12 3l8 4"/></svg>',
    "casa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.8V21h14V9.8"/><path d="M9.5 21v-6h5v6"/></svg>',
    "escudo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.5 4 6v6c0 5 3.4 8.6 8 9.5 4.6-.9 8-4.5 8-9.5V6z"/></svg>',
    "auto": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14l1.4-5.6a2 2 0 0 0-.8-2.1l-1.3-.9-1.5-3A2 2 0 0 0 15 4.3H9a2 2 0 0 0-1.8 1.1l-1.5 3-1.3.9a2 2 0 0 0-.8 2.1z"/><circle cx="7.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/></svg>',
    "pergamino": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h11a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5"/><path d="M9 8h7M9 12h7M9 16h4"/></svg>',
    "edificio": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/></svg>',
    "billete": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/></svg>',
    "estado": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9.5 12 4l9 5.5"/><path d="M5 10v8M9.7 10v8M14.3 10v8M19 10v8M3 21h18"/></svg>',
    "estrella": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2.6 2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3-5.8 3 1.1-6.5L2.6 9.4l6.5-.9z"/></svg>',
    "google": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.9h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.4z"/><path fill="#34A853" d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.7-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z"/><path fill="#FBBC05" d="M6.4 14c-.2-.6-.3-1.3-.3-2s.1-1.4.3-2V7.4H3.1a10 10 0 0 0 0 9.2z"/><path fill="#EA4335" d="M12 5.9c1.5 0 2.8.5 3.8 1.5l2.8-2.8A10 10 0 0 0 3.1 7.4L6.4 10c.8-2.4 3-4.1 5.6-4.1z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.5 3c.3 2 1.5 3.5 3.5 3.8v2.6c-1.3.1-2.5-.3-3.6-1v6.3c0 3.2-2.4 5.6-5.5 5.6S5.4 17.9 5.4 14.8s2.4-5.6 5.5-5.6c.3 0 .6 0 .9.1v2.7c-.3-.1-.6-.1-.9-.1-1.6 0-2.8 1.3-2.8 2.9s1.2 2.9 2.8 2.9 2.9-1.3 2.9-2.9V3z"/></svg>',
}

# ------------------------------------------------------------------ contenido

# Secciones de la landing, en el orden del diseño.
# (ancla, etiqueta larga, etiqueta corta para la barra de escritorio).
# Con etiqueta corta None la sección no entra en la barra, pero sigue en el
# menú a pantalla completa y en el pie: siete ítems de dos palabras no entran.
SECCIONES = [
    ("inicio", "Inicio", None),
    ("sobre-mi", "Sobre mí", "Sobre mí"),
    ("areas", "Áreas de práctica", "Áreas"),
    ("por-que", "Por qué elegirnos", None),
    ("resenas", "Reseñas", "Reseñas"),
    ("proceso", "Cómo trabajamos", "Proceso"),
    ("zonas", "Dónde atendemos", None),
    ("preguntas", "Preguntas frecuentes", "Preguntas"),
    ("contacto", "Contacto", "Contacto"),
]

# Las 10 áreas del documento del cliente.
# Descripción [D] = literal del diseño · [AS] = redactada por AS BIT.
AREAS = [
    ("maletin", "Derecho Laboral", "D",
     "Consultas y representación en conflictos laborales, tanto para trabajadores como para empleadores. Indemnizaciones, despidos, contratos de trabajo.",
     "derecho laboral"),
    ("familia", "Derecho de Familia", "D",
     "Divorcios, pensiones alimenticias, tenencia y régimen de visitas. Acompañamiento con sensibilidad en momentos difíciles.",
     "derecho de familia"),
    ("escudo", "Derecho Penal", "D",
     "Defensa y representación legal en causas penales, con atención inmediata cuando el tiempo es crítico.",
     "derecho penal"),
    ("balanza", "Derecho Civil", "AS",
     "Contratos, deudas y cobros, daños y perjuicios, desalojos, arrendamientos y cartas documento.",
     "derecho civil"),
    ("casa", "Derecho Inmobiliario", "AS",
     "Usucapión, compraventa de inmuebles, escrituración, títulos de propiedad y loteos.",
     "derecho inmobiliario"),
    ("auto", "Accidentes de Tránsito", "AS",
     "Reclamos por accidentes, seguros, lesiones y daños a vehículos, incluidos los juicios contra aseguradoras.",
     "un accidente de tránsito"),
    ("pergamino", "Sucesiones y Herencias", "AS",
     "Declaratoria de herederos, testamentos, división de bienes y herencias en conflicto.",
     "una sucesión o herencia"),
    ("edificio", "Comercial y Empresarial", "AS",
     "Constitución de empresas (SRL, SA), contratos comerciales, deudas entre empresas y quiebras.",
     "un tema comercial o empresarial"),
    ("billete", "Deudas y Cobranzas", "AS",
     "Pagarés, cheques sin fondos, deudas bancarias, reclamos a financieras y negociación con acreedores.",
     "una deuda o cobranza"),
    ("estado", "Derecho Administrativo", "AS",
     "Trámites con el Estado, multas, licitaciones y recursos contra organismos públicos.",
     "un trámite administrativo"),
]

# [AS] los tres pilares salen textualmente del párrafo del hero del diseño:
# "atención directa, sin letra chica y consultas a domicilio".
VENTAJAS = [
    ("Atención directa", "Su caso lo lleva el abogado. Habla con él desde el primer mensaje y en cada etapa del proceso, sin intermediarios."),
    ("Sin letra chica", "Le explicamos en términos claros qué se puede hacer, qué no, y qué pasos implica cada opción antes de avanzar."),
    ("Consultas a domicilio", "Si no puede acercarse al estudio, coordinamos la consulta donde usted esté, en %s y alrededores." % CIUDAD),
]

# Paso 1 [AS], pasos 2 a 4 [D] literales del diseño.
PROCESO = [
    ("Primer contacto", "Nos escribe por WhatsApp y nos cuenta su situación, con sus palabras y sin formalidades."),
    ("Análisis del caso", "Se revisa la documentación y se evalúan las opciones legales disponibles."),
    ("Estrategia", "Se define el camino a seguir, explicado en términos claros, con los tiempos y pasos esperables."),
    ("Acompañamiento", "Seguimiento constante durante todo el proceso, con comunicación directa en cada etapa."),
]

# Preguntas [D] literales. Respuesta 1 [D] literal; 2 a 5 [AS].
FAQ = [
    ("¿Cuánto cuesta la primera consulta?",
     "El costo se informa al coordinarla. Escríbanos por WhatsApp y le contamos los detalles según su caso."),
    ("¿En qué zonas atienden?",
     "Atendemos en %s y en todo el %s. También coordinamos consultas a domicilio." % (CIUDAD, REGION)),
    ("¿Puedo hacer la consulta por WhatsApp?",
     "Sí. Es la vía más rápida y le responde el abogado directamente, sin intermediarios."),
    ("¿Cuánto tarda un proceso legal?",
     "Depende del tipo de caso y de la vía que se elija. En la primera consulta le damos un plazo estimado realista y le explicamos qué puede acortarlo o alargarlo."),
    ("¿Atienden fuera del horario de oficina?",
     "El horario de atención es de %s. Si escribe fuera de ese horario, le respondemos apenas retomamos." % HORARIO.lower()),
]

# ------------------------------------------------------------------ JSON-LD


def jsonld_negocio():
    servicios = ",\n      ".join(
        '{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "%s", "serviceType": "%s"}}'
        % (nombre, nombre) for _ic, nombre, _o, _d, _wa in AREAS
    )
    zonas = ",\n".join(
        '    {"@type": "City", "name": "%s"}' % z for z in ZONAS
    ) + ',\n    {"@type": "AdministrativeArea", "name": "%s, Paraguay"}' % REGION

    plantilla_resena = (
        '    {"@type": "Review",\n'
        '     "reviewRating": {"@type": "Rating", "ratingValue": "%d", "bestRating": "5"},\n'
        '     "author": {"@type": "Person", "name": "%s"},\n'
        '     "reviewBody": "%s"}'
    )
    resenas = ",\n".join(
        plantilla_resena % (nota, autor, texto)
        for autor, nota, texto, _resp in RESENAS
    )
    return """{
  "@context": "https://schema.org",
  "@type": "Attorney",
  "@id": "%(base)s#estudio",
  "name": "Estudio Jurídico Abog. Blas Santander",
  "alternateName": ["Estudio Jurídico Santander", "Estudio Juridico Abog. Blas Santander-servicios legales"],
  "description": "Asesoría legal en %(ciudad)s, Paraguay. Derecho laboral, de familia, penal, civil, inmobiliario, accidentes de tránsito, sucesiones, comercial, cobranzas y administrativo.",
  "image": "%(base)sassets/img/blas-santander.jpg",
  "logo": "%(base)sassets/img/logo.png",
  "url": "%(base)s",
  "telephone": "%(tel)s",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "%(calle)s",
    "addressLocality": "%(ciudad)s",
    "postalCode": "%(cp)s",
    "addressRegion": "Central",
    "addressCountry": "PY"
  },
  "geo": {"@type": "GeoCoordinates", "latitude": -25.3805, "longitude": -57.525071},
  "hasMap": "%(mapa)s",
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "opens": "%(abre)s",
    "closes": "%(cierra)s"
  }],
  "areaServed": [
%(zonas)s
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "%(prom)s",
    "reviewCount": "%(total)s",
    "bestRating": "5"
  },
  "review": [
%(resenas)s
  ],
  "founder": {"@type": "Person", "name": "Blas Santander", "jobTitle": "Abogado"},
  "employee": {"@type": "Person", "name": "Blas Santander", "jobTitle": "Abogado"},
  "knowsLanguage": ["es-PY", "gn"],
  "availableLanguage": ["Español", "Guaraní"],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Áreas de práctica",
    "itemListElement": [
      %(servicios)s
    ]
  },
  "sameAs": ["%(ig)s", "%(tk)s", "%(gmb)s"]
}""" % {
        "base": BASE, "tel": TEL_E164, "ciudad": CIUDAD, "region": REGION,
        "abre": HORARIO_ABRE, "cierra": HORARIO_CIERRA,
        "calle": CALLE, "cp": CP, "mapa": GOOGLE_MAPA,
        "ig": IG, "tk": TIKTOK, "gmb": GOOGLE_PERFIL, "servicios": servicios,
        "zonas": zonas, "prom": RESENAS_PROMEDIO, "total": RESENAS_TOTAL,
        "resenas": resenas,
    }


def jsonld_faq():
    entradas = ",\n    ".join(
        '{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}'
        % (p, r) for p, r in FAQ
    )
    return """{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    %s
  ]
}""" % entradas


JSONLD_SITIO = """{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Estudio Jurídico Abog. Blas Santander",
  "url": "%(base)s",
  "inLanguage": "es-PY",
  "publisher": {"@id": "%(base)s#estudio"}
}""" % {"base": BASE}

# ------------------------------------------------------------------ parciales


def head(titulo, descripcion, ruta, jsonld, precarga_hero=False, robots=None):
    canonical = BASE + ("" if ruta == "index.html" else ruta)
    og_img = BASE + "assets/img/logo.png"
    robots = robots or "index, follow, max-image-preview:large, max-snippet:-1"

    precarga = ""
    if precarga_hero:
        precarga = (
            '\n<link rel="preload" as="image" href="assets/img/hero-madera-900.jpg"'
            ' imagesrcset="assets/img/hero-madera-900.jpg 900w, assets/img/hero-madera-1600.jpg 1600w"'
            ' imagesizes="100vw" fetchpriority="high">'
        )

    bloques = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' % j.strip() for j in jsonld
    )

    return """<!DOCTYPE html>
<html lang="es-PY">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="%(robots)s">
<meta name="author" content="Blas Santander">
<meta name="geo.region" content="PY-11">
<meta name="geo.placename" content="%(ciudad)s, %(region)s, Paraguay">
<meta name="theme-color" content="#0E0F12">
<meta name="google-site-verification" content="%(gsc)s">
<link rel="canonical" href="%(canonical)s">
<link rel="alternate" hreflang="es-py" href="%(canonical)s">
<link rel="alternate" hreflang="x-default" href="%(canonical)s">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Estudio Jurídico Abog. Blas Santander">
<meta property="og:locale" content="es_PY">
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(og)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(titulo)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og)s">

<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/icon-180.png">
<link rel="manifest" href="site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Nunito+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">%(precarga)s
<noscript><style>
  /* Si el JavaScript no carga, nada debe quedar invisible esperándolo. */
  .rv,.rv--esc>*{opacity:1 !important;transform:none !important}
  .hero .anim{opacity:1 !important;transform:none !important}
  .resenas__estrellas svg{opacity:1 !important;transform:none !important}
  .faq__panel{grid-template-rows:1fr !important}
  .cta-fija{display:none !important}
</style></noscript>

%(jsonld)s

<!-- Google tag (gtag.js) — GA4. Mientras GA4_ID tenga XXXX no se carga nada. -->
<script>
  window.GA4_ID = "%(ga4)s";
  if (window.GA4_ID.indexOf("XXXX") === -1) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + window.GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", window.GA4_ID);
  }
</script>
</head>
<body>
<a href="#principal" class="salto-link">Saltar al contenido</a>
<div class="barra-progreso" aria-hidden="true"></div>
""" % {
        "titulo": titulo, "desc": descripcion, "canonical": canonical, "og": og_img,
        "gsc": GSC_TOKEN, "jsonld": bloques, "precarga": precarga, "ga4": GA4_ID,
        "robots": robots, "ciudad": CIUDAD, "region": REGION,
    }


def cabecera(interna=False):
    pre = "index.html" if interna else ""
    esc = "\n      ".join(
        '<a href="%s#%s">%s</a>' % (pre, slug, corto)
        for slug, _largo, corto in SECCIONES if corto
    )
    items = "\n    ".join(
        '<a href="%s#%s"><span class="num">%02d</span>%s</a>' % (pre, slug, i, largo)
        for i, (slug, largo, _corto) in enumerate(SECCIONES, start=1)
    )

    return """<header class="cabecera">
  <div class="contenedor">
    <a href="%(inicio)s" class="marca" aria-label="Estudio Jurídico Santander — Inicio">
      <span class="marca__escudo"><img src="assets/img/logo.png" alt="" width="42" height="42"></span>
      <span class="marca__texto">
        <strong>Estudio Jurídico Santander</strong>
        <small>Abogado</small>
      </span>
    </a>
    <nav class="nav-esc" aria-label="Navegación principal">
      %(esc)s
    </nav>
    <div class="acciones-cabecera">
      <a class="btn btn--sm btn-wa-cabecera" href="%(wa)s" target="_blank" rel="noopener" data-wa="cabecera">
        %(i_wa)s<span>WhatsApp</span>
      </a>
      <button class="hamburguesa" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<nav class="menu" id="menu" data-abierto="false" aria-label="Menú principal">
  <div class="menu__lista">
    %(items)s
  </div>
  <div class="menu__pie">
    <p class="dato-menu">WhatsApp directo<b>%(tel)s</b></p>
    <p class="dato-menu">%(horario)s · Consultas a domicilio</p>
    <a class="btn btn--bloque" href="%(wa)s" target="_blank" rel="noopener" data-wa="menu">
      %(i_wa)s<span>Escribir por WhatsApp</span>
    </a>
  </div>
</nav>
""" % {
        "inicio": "index.html" if interna else "#inicio",
        "esc": esc, "items": items, "wa": WA_GENERAL, "i_wa": I["wa"],
        "tel": TEL_LINDO, "horario": HORARIO,
    }


def pie(interna=False):
    pre = "index.html" if interna else ""
    nav = "\n      ".join(
        '<a href="%s#%s">%s</a>' % (pre, slug, largo)
        for slug, largo, _corto in SECCIONES
    )
    return """<footer class="pie">
  <div class="contenedor">
    <img class="pie__escudo" src="assets/img/logo.png" alt="Emblema del Estudio Jurídico Abog. Blas Santander" width="78" height="71" loading="lazy">
    <p class="pie__lema">Estudio Jurídico Abog. Blas Santander — Asesoría legal en %(ciudad)s</p>
    <p class="pie__linea">
      <a href="tel:%(tel_e164)s">%(tel)s</a> · %(direccion)s · %(horario)s
    </p>

    <nav class="pie__nav" aria-label="Navegación del pie">
      %(nav)s
    </nav>

    <div class="pie__redes">
      <a href="%(ig)s" target="_blank" rel="noopener" aria-label="Instagram del estudio">%(i_ig)s</a>
      <a href="%(tk)s" target="_blank" rel="noopener" aria-label="TikTok del estudio">%(i_tk)s</a>
      <a href="%(wa)s" target="_blank" rel="noopener" aria-label="WhatsApp del estudio" data-wa="pie">%(i_wa)s</a>
    </div>

    <p class="pie__legal">
      © <span data-anio>2026</span> Estudio Jurídico Abog. Blas Santander. Todos los derechos reservados.<br>
      %(ciudad)s, %(region)s, Paraguay
      <br><a class="pie__asbit" href="https://asbit.com.py" target="_blank" rel="noopener">Web desarrollada por AS BIT</a>
    </p>
  </div>
</footer>

<div class="cta-fija" data-visible="false" aria-hidden="true">
  <a class="btn btn--bloque" href="%(wa)s" target="_blank" rel="noopener" data-wa="fija">
    %(i_wa)s<span>Consulta por WhatsApp</span>
  </a>
</div>

<script src="assets/js/main.js" defer></script>
</body>
</html>
""" % {
        "ciudad": CIUDAD, "region": REGION, "tel": TEL_LINDO, "horario": HORARIO,
        "tel_e164": TEL_E164, "direccion": DIRECCION,
        "nav": nav, "ig": IG, "tk": TIKTOK, "wa": WA_GENERAL,
        "i_ig": I["ig"], "i_tk": I["tiktok"], "i_wa": I["wa"],
    }

# ------------------------------------------------------------------ landing


def landing():
    chips = "".join(
        '<a class="chip" href="#areas">%s</a>' % nombre
        for _ic, nombre, _o, _d, _wa in AREAS
    )

    tarjetas = "\n        ".join(
        """<a class="tarjeta" href="%(wa)s" target="_blank" rel="noopener" data-wa="area-%(n)d">
          <span class="tarjeta__icono">%(icono)s</span>
          <h3>%(nombre)s</h3>
          <p>%(desc)s</p>
          <span class="enlace-oro">Consultar %(flecha)s</span>
        </a>""" % {
            "wa": wa_link("Hola, quisiera hacer una consulta sobre %s." % msg),
            "n": n, "icono": I[ic], "nombre": nombre, "desc": desc, "flecha": I["flecha"],
        }
        for n, (ic, nombre, _o, desc, msg) in enumerate(AREAS, start=1)
    )

    ventajas = "\n        ".join(
        """<div class="ventaja">
          <span class="ventaja__num">%02d</span>
          <h3>%s</h3>
          <p>%s</p>
        </div>""" % (n, t, d) for n, (t, d) in enumerate(VENTAJAS, start=1)
    )

    pasos = "\n      ".join(
        """<div class="paso">
        <span class="paso__n">%d</span>
        <div><h3>%s</h3><p>%s</p></div>
      </div>""" % (n, t, d) for n, (t, d) in enumerate(PROCESO, start=1)
    )

    # tarjetas de reseña, con el texto tal cual lo publicó cada cliente
    tarjeta_resena = (
        '<figure class="resena-card">\n'
        '          <div class="resena-card__estrellas" role="img" aria-label="%(nota)d de 5 estrellas">%(estrellas)s</div>\n'
        '          <blockquote>%(texto)s</blockquote>\n'
        '          <figcaption>%(autor)s <span>· en Google</span></figcaption>\n'
        '          %(respuesta)s\n'
        '        </figure>'
    )
    resenas_html = "\n        ".join(
        tarjeta_resena % {
            "nota": nota,
            "estrellas": I["estrella"] * nota,
            "texto": texto,
            "autor": autor,
            "respuesta": ('<p class="resena-card__respuesta"><span>Respuesta del estudio</span>%s</p>' % resp)
                         if resp else "",
        }
        for autor, nota, texto, resp in RESENAS
    )

    zonas_html = "\n        ".join('<li>%s</li>' % z for z in ZONAS)

    faq = "\n    ".join(
        """<div class="faq__item" data-abierto="%(a)s">
      <h3><button class="faq__boton" type="button" aria-expanded="%(a)s" id="faq-b%(i)d" aria-controls="faq-p%(i)d">%(p)s<span class="faq__signo" aria-hidden="true"></span></button></h3>
      <div class="faq__panel" id="faq-p%(i)d" role="region" aria-labelledby="faq-b%(i)d"><div><p>%(r)s</p></div></div>
    </div>""" % {"a": "true" if i == 0 else "false", "i": i, "p": p, "r": r}
        for i, (p, r) in enumerate(FAQ)
    )

    cuerpo = """%(cabecera)s

<main id="principal">

  <!-- ===== HERO — texto literal del diseño ===== -->
  <section class="hero" id="inicio">
    <div class="hero__fondo">
      <img src="assets/img/hero-madera-900.jpg"
           srcset="assets/img/hero-madera-900.jpg 900w, assets/img/hero-madera-1600.jpg 1600w"
           sizes="100vw" alt="" aria-hidden="true" width="1600" height="2400" fetchpriority="high">
    </div>
    <div class="hero__velo" aria-hidden="true"></div>
    <div class="contenedor">
      <div class="hero__cuerpo">
        <p class="eyebrow anim" style="--d:80ms">%(ciudad)s · Paraguay</p>
        <h1 class="anim" style="--d:180ms">Asesoría legal clara, cercana y <em>comprometida</em> con su caso.</h1>
        <p class="hero__plomo anim" style="--d:300ms">El Estudio Jurídico Abog. Blas Santander acompaña a personas y empresas en %(ciudad)s y alrededores en sus procesos legales, con atención directa, sin letra chica y consultas a domicilio.</p>
        <div class="hero__ctas anim" style="--d:420ms" data-ctas-hero>
          <a class="btn" href="#contacto">Solicitar una consulta</a>
          <a class="btn btn--linea" href="%(wa)s" target="_blank" rel="noopener" data-wa="hero">%(i_wa)s<span>Escribir por WhatsApp</span></a>
        </div>
        <p class="hero__sellos anim" style="--d:540ms">
          <span><i class="pip" aria-hidden="true"></i>Más de 10 años de experiencia</span>
          <span><i class="pip" aria-hidden="true"></i>%(ciudad)s y todo el %(region)s</span>
          <span class="sello--horario"><i class="pip" aria-hidden="true"></i>%(horario)s</span>
        </p>
      </div>

      <!-- Burbuja de horario: ocupa el aire de la derecha en escritorio.
           En móvil no aparece; el dato ya está en los sellos del hero. -->
      <aside class="burbuja" aria-label="Horario de atención">
        <span class="burbuja__icono">%(i_reloj)s</span>
        <p class="burbuja__rotulo">Horario de atención</p>
        <p class="burbuja__dias">Lunes a sábados</p>
        <p class="burbuja__hora">7:00 <span>a</span> 17:00</p>
        <p class="burbuja__extra">%(i_casa)s Consultas a domicilio</p>
      </aside>
    </div>
  </section>

  <div class="marquesina" aria-label="Áreas de práctica">
    <div class="marquesina__pista">%(chips)s</div>
  </div>

  <!-- ===== SOBRE MÍ ===== -->
  <section class="seccion seccion--marfil" id="sobre-mi">
    <div class="contenedor">
      <div class="sobre">
        <div class="sobre__figura rv">
          <img src="assets/img/blas-santander-900.jpg" alt="Abog. Blas Santander, abogado en %(ciudad)s, Paraguay" width="585" height="853" loading="lazy">
        </div>
        <div class="rv" style="--d:120ms">
          <p class="eyebrow">Sobre mí</p>
          <h2>Quién lo va a representar</h2>
          <p class="plomo">Blas Santander es abogado con más de diez años de ejercicio, acompañando a personas y familias de %(ciudad)s y de todo el %(region)s en sus problemas legales. Atiende personalmente cada caso, explica cada paso en términos claros y coordina consultas a domicilio cuando hace falta.</p>
          <div class="sobre__cifra">
            <span class="n" data-contador="10" data-prefijo="+">+10</span>
            <span class="t">años de experiencia ejerciendo el derecho</span>
          </div>
          <p class="sobre__firma">Abog. Blas Santander<small>%(ciudad)s · %(region)s</small></p>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== ÁREAS ===== -->
  <section class="seccion" id="areas">
    <div class="contenedor">
      <div class="encabezado-seccion rv">
        <p class="eyebrow">Áreas de práctica</p>
        <h2>En qué podemos ayudarlo</h2>
        <p class="plomo">Diez áreas del derecho, atendidas en %(ciudad)s y en todo el %(region)s. Toque cualquiera para consultar por WhatsApp.</p>
        <div class="filete" aria-hidden="true"></div>
      </div>
      <div class="rejilla rejilla--2 rejilla--3 rv--esc">
        %(tarjetas)s
      </div>
    </div>
  </section>

  <!-- ===== POR QUÉ ===== -->
  <section class="seccion seccion--carbon" id="por-que">
    <div class="contenedor">
      <div class="encabezado-seccion rv">
        <p class="eyebrow">Por qué elegirnos</p>
        <h2>Por qué trabajar con nosotros</h2>
      </div>
      <div class="ventajas rv--esc">
        %(ventajas)s
      </div>
    </div>
  </section>

  <!-- ===== RESEÑAS DE GOOGLE (opiniones reales del Perfil de Empresa) ===== -->
  <section class="seccion" id="resenas">
    <div class="contenedor">
      <div class="encabezado-seccion rv">
        <p class="eyebrow">Reseñas</p>
        <h2>Lo que dicen quienes ya pasaron por acá</h2>
        <p class="plomo">Opiniones publicadas por clientes en el Perfil de Empresa del estudio en Google. Ninguna está escrita por nosotros: se pueden verificar una por una.</p>
      </div>

      <div class="marca-google rv">
        <div class="marca-google__nota">%(prom_visible)s</div>
        <div>
          <div class="marca-google__estrellas" role="img" aria-label="Calificación %(prom_visible)s sobre 5 en Google">%(estrellas5)s</div>
          <p class="marca-google__pie">%(total)s opiniones en Google · %(i_google)s <span>Perfil verificado</span></p>
        </div>
      </div>

      <div class="rejilla rejilla--2 rv--esc" style="margin-top:20px">
        %(resenas_html)s
      </div>

      <div class="destaque-google rv">
        <p class="eyebrow">Presencia en Google</p>
        <p>Cuando alguien busca <strong>«abogado en %(ciudad)s»</strong> en Google, el estudio aparece entre los primeros resultados del mapa. No es casualidad: es un perfil trabajado, con los datos al día, las áreas cargadas y reseñas reales de clientes.</p>
      </div>

      <div class="resenas__ctas rv">
        <a class="btn" href="%(resena)s" target="_blank" rel="noopener" data-ev="resena_escribir">%(i_estrella)s<span>Dejar una reseña</span></a>
        <a class="btn btn--linea" href="%(ver)s" target="_blank" rel="noopener" data-ev="resena_ver">%(i_google)s<span>Ver todas en Google</span></a>
      </div>
      <p class="resenas__nota rv">¿El estudio lo acompañó en un caso? Contar su experiencia toma menos de un minuto y ayuda a la próxima persona que esté buscando con quién hablar.</p>
    </div>
  </section>

  <!-- ===== ZONAS ===== -->
  <section class="seccion seccion--marfil" id="zonas">
    <div class="contenedor">
      <div class="encabezado-seccion rv">
        <p class="eyebrow">Dónde atendemos</p>
        <h2>%(ciudad)s y todo el %(region)s</h2>
        <p class="plomo">El estudio está sobre %(calle)s, en %(ciudad)s, y atiende casos de todo el %(region)s. Si no puede acercarse, coordinamos la consulta a domicilio.</p>
      </div>
      <ul class="zonas rv--esc">
        %(zonas_html)s
      </ul>
      <p class="zonas__nota rv">¿Su caso es de otra ciudad? Consúltenos igual: muchos trámites se resuelven sin que usted tenga que viajar.</p>
    </div>
  </section>

  <!-- ===== PROCESO ===== -->
  <section class="seccion seccion--carbon" id="proceso">
    <div class="contenedor">
      <div class="proceso rv">
        <div>
          <p class="eyebrow">Proceso</p>
          <h2>Cómo trabajamos</h2>
          <p class="proceso__intro">Cuatro etapas, explicadas de antemano, para que sepa siempre en qué punto está su caso.</p>
        </div>
        <div class="proceso__pasos">
        %(pasos)s
        </div>
      </div>
    </div>
  </section>

  <!-- ===== FAQ ===== -->
  <section class="seccion seccion--carbon" id="preguntas">
    <div class="contenedor">
      <div class="encabezado-seccion rv">
        <p class="eyebrow">Preguntas frecuentes</p>
        <h2>Preguntas frecuentes</h2>
      </div>
      <div class="faq rv">
    %(faq)s
      </div>
    </div>
  </section>

  <!-- ===== CONTACTO ===== -->
  <section class="seccion" id="contacto">
    <div class="contenedor">
      <div class="contacto rv">
        <img class="contacto__escudo" src="assets/img/logo.png" alt="" aria-hidden="true" loading="lazy" width="280" height="254">
        <div>
          <p class="eyebrow">Contacto</p>
          <h2>Hablemos de su caso</h2>
          <p class="plomo">Cuéntenos su situación y le respondemos a la brevedad. La primera consulta es el paso para entender sus opciones legales. También coordinamos consultas a domicilio.</p>

          <div class="datos">
            <div class="dato">
              %(i_wa_chico)s
              <div><span class="rotulo">WhatsApp</span><a class="valor" href="%(wa)s" target="_blank" rel="noopener" data-wa="contacto">%(tel)s</a></div>
            </div>
            <div class="dato">
              %(i_mapa)s
              <div>
                <span class="rotulo">Dirección</span>
                <a class="valor valor--chico dato__mapa" href="%(mapa)s" target="_blank" rel="noopener" data-ev="como_llegar_dato">%(direccion)s</a>
                <span class="dato__extra">Atención en todo el %(region)s y consultas a domicilio</span>
              </div>
            </div>
            <div class="dato">
              %(i_reloj)s
              <div><span class="rotulo">Horario de atención</span><span class="valor valor--chico">%(horario)s</span></div>
            </div>
          </div>

          <div class="contacto__ctas">
            <a class="btn" href="%(wa)s" target="_blank" rel="noopener" data-wa="contacto-btn">%(i_wa)s<span>Escribir por WhatsApp</span></a>
            <a class="btn btn--linea" href="%(mapa)s" target="_blank" rel="noopener" data-ev="como_llegar">%(i_mapa_chico)s<span>Cómo llegar</span></a>
          </div>
        </div>

        <div>
          <form class="formulario" id="form-consulta" novalidate>
            <div class="campo">
              <label for="nombre">Nombre</label>
              <input id="nombre" name="nombre" type="text" autocomplete="name" required>
            </div>
            <div class="campo">
              <label for="telefono">Teléfono</label>
              <input id="telefono" name="telefono" type="tel" autocomplete="tel" inputmode="tel">
            </div>
            <div class="campo campo--ancho">
              <label for="caso">Cuéntenos su caso</label>
              <textarea id="caso" name="caso" rows="4"></textarea>
            </div>
            <button class="btn btn--bloque" type="submit">%(i_wa)s<span>Enviar por WhatsApp</span></button>
            <p class="nota-form campo--ancho">Al enviar se abre WhatsApp con su mensaje ya redactado, para que lo confirme usted.</p>
            <p class="form-ok campo--ancho" id="form-ok" data-visible="false" role="status">Listo, se abrió WhatsApp con su mensaje. Si no se abrió solo, escríbanos al %(tel)s.</p>
          </form>
        </div>
      </div>
    </div>
  </section>

</main>
""" % {
        "cabecera": cabecera(), "ciudad": CIUDAD, "region": REGION, "horario": HORARIO,
        "wa": WA_GENERAL, "i_wa": I["wa"], "i_tel": I["tel"], "i_mapa": I["mapa"],
        "i_reloj": I["reloj"], "tel": TEL_LINDO,
        "chips": chips, "tarjetas": tarjetas, "ventajas": ventajas, "pasos": pasos, "faq": faq,
        "i_estrella": I["estrella"], "i_google": I["google"],
        "resena": GOOGLE_RESENA, "ver": GOOGLE_VER_RESENAS,
        "resenas_html": resenas_html, "zonas_html": zonas_html,
        "estrellas5": I["estrella"] * 5,
        "prom_visible": RESENAS_PROMEDIO.replace(".", ","),
        "total": RESENAS_TOTAL,
        "direccion": DIRECCION, "calle": CALLE, "mapa": GOOGLE_MAPA,
        "tel_e164": TEL_E164, "i_mapa_chico": I["mapa"], "i_wa_chico": I["wa"],
        "i_casa": I["casa"],
    }

    cabeza = head(
        "Abogado en %s | Estudio Jurídico Abog. Blas Santander" % CIUDAD,
        "Abogado en %s, %s. Más de 10 años en derecho laboral, familia, penal, civil, "
        "inmobiliario, tránsito y sucesiones. Atención directa y consultas a domicilio. "
        "Escríbanos por WhatsApp." % (CIUDAD, REGION),
        "index.html",
        [jsonld_negocio(), JSONLD_SITIO, jsonld_faq()],
        precarga_hero=True,
    )
    return cabeza + cuerpo + pie()


def pagina_404():
    cuerpo = """%s

<main id="principal">
  <section class="cabecera-pagina" style="padding-top:calc(var(--nav-h) + 70px);text-align:center">
    <div class="contenedor">
      <p class="eyebrow">Error 404</p>
      <h1 style="max-width:20ch;margin-inline:auto">Esta página no existe o cambió de dirección</h1>
      <p class="plomo" style="max-width:48ch;margin:0 auto 28px">Puede que el enlace esté desactualizado. Vuelva al inicio o escríbanos y lo ayudamos.</p>
      <a class="btn" href="index.html">Volver al inicio</a>
    </div>
  </section>
</main>
""" % cabecera(interna=True)

    cabeza = head(
        "Página no encontrada | Estudio Jurídico Abog. Blas Santander",
        "La página que busca no existe. Vuelva al inicio del sitio del Estudio Jurídico Abog. Blas Santander.",
        "404.html", [], robots="noindex, follow",
    )
    return cabeza + cuerpo + pie(interna=True)

# ------------------------------------------------------------------ salida

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
""" % (BASE, date.today().isoformat())

ROBOTS = """User-agent: *
Allow: /

Sitemap: %ssitemap.xml
""" % BASE

MANIFEST = """{
  "name": "Estudio Jurídico Abog. Blas Santander",
  "short_name": "Abog. Santander",
  "description": "Asesoría legal en %s, Paraguay.",
  "lang": "es-PY",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#0E0F12",
  "theme_color": "#0E0F12",
  "icons": [
    {"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
""" % CIUDAD


def escribir(nombre, contenido):
    with io.open(nombre, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)
    print("  %-22s %6d bytes" % (nombre, len(contenido.encode("utf-8"))))


def main():
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(raiz)
    print("Generando el sitio en %s" % raiz)
    escribir("index.html", landing())
    escribir("404.html", pagina_404())
    escribir("sitemap.xml", SITEMAP)
    escribir("robots.txt", ROBOTS)
    escribir("site.webmanifest", MANIFEST)
    print("Listo.")


if __name__ == "__main__":
    main()
