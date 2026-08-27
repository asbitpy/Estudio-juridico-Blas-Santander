/* ==========================================================================
   Estudio Jurídico Blas Edgar Santander — Interacciones
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Menú móvil ---------- */
  var navToggle = document.querySelector('.nav-toggle');
  var mobileNav = document.querySelector('.mobile-nav');

  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      var isOpen = mobileNav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---------- Scroll reveal ----------
     Nunca debe quedar contenido invisible: un salto de scroll grande
     (fling en mobile, click en un link de ancla, scroll muy rápido)
     puede hacer que un elemento pase de "abajo del todo" a "arriba del
     todo" en un solo frame y el IntersectionObserver no llegue a
     marcarlo. Por eso el reveal se refuerza con tres capas: observer
     con margen amplio, un chequeo por posición en cada scroll/resize,
     y una red de seguridad que fuerza todo visible a los 2s. */
  var revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    var showEl = function (el) {
      if (el.classList.contains('is-visible')) return;
      var delay = el.getAttribute('data-delay') || 0;
      setTimeout(function () { el.classList.add('is-visible'); }, Number(delay));
    };

    var revealIfPassed = function () {
      var vh = window.innerHeight;
      revealEls.forEach(function (el) {
        if (el.classList.contains('is-visible')) return;
        var rect = el.getBoundingClientRect();
        // Ya entró en pantalla, o el usuario ya scrolleó más allá de él:
        // en ambos casos no tiene sentido seguir ocultándolo.
        if (rect.top < vh && rect.bottom > 0) showEl(el);
        else if (rect.bottom <= 0) showEl(el);
      });
    };

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              showEl(entry.target);
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0, rootMargin: '200px 0px -10% 0px' }
      );
      revealEls.forEach(function (el) { observer.observe(el); });
    }

    // Red de seguridad: revisa por posición real en cada scroll/resize
    // (cubre saltos grandes que el observer puede perder) y una vez al
    // cargar, por si el usuario entra ya scrolleado (anchor link).
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { revealIfPassed(); ticking = false; });
    }, { passive: true });
    window.addEventListener('resize', revealIfPassed);
    revealIfPassed();

    // Última red de seguridad: nada debe quedar oculto para siempre.
    setTimeout(function () { revealEls.forEach(showEl); }, 2000);
  }

  /* ---------- Acordeón Otras Áreas ---------- */
  var accordionHeaders = document.querySelectorAll('.accordion-header');
  accordionHeaders.forEach(function (header) {
    header.addEventListener('click', function () {
      var expanded = header.getAttribute('aria-expanded') === 'true';
      var panel = document.getElementById(header.getAttribute('aria-controls'));

      // Cerrar los demás (comportamiento tipo índice de libro, uno a la vez)
      accordionHeaders.forEach(function (otherHeader) {
        if (otherHeader !== header) {
          otherHeader.setAttribute('aria-expanded', 'false');
          var otherPanel = document.getElementById(otherHeader.getAttribute('aria-controls'));
          if (otherPanel) {
            otherPanel.classList.remove('is-open');
            otherPanel.style.maxHeight = null;
          }
        }
      });

      header.setAttribute('aria-expanded', String(!expanded));
      if (!expanded) {
        panel.classList.add('is-open');
        panel.style.maxHeight = panel.scrollHeight + 40 + 'px';
      } else {
        panel.classList.remove('is-open');
        panel.style.maxHeight = null;
      }
    });
  });

  /* ---------- Formulario de contacto (sin backend: prepara envío por WhatsApp) ---------- */
  var contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var nombre = document.getElementById('nombre').value.trim();
      var telefono = document.getElementById('telefono').value.trim();
      var mensaje = document.getElementById('mensaje').value.trim();

      var texto =
        'Hola, soy ' + nombre + ' (tel: ' + telefono + '). ' + mensaje;
      var url = 'https://wa.me/595984750151?text=' + encodeURIComponent(texto);

      var successBox = document.getElementById('form-success');
      if (successBox) successBox.classList.add('is-visible');

      window.open(url, '_blank', 'noopener');
      contactForm.reset();
    });
  }

  /* ---------- Año actual en footer ---------- */
  var yearEls = document.querySelectorAll('.current-year');
  yearEls.forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
