/* =========================================================
   Estudio Jurídico Abog. Blas Santander
   Interacciones y animaciones — sin dependencias
   ========================================================= */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Menú a pantalla completa ---------- */
  var boton = document.querySelector('.hamburguesa');
  var menu = document.getElementById('menu');

  function cerrarMenu() {
    if (!menu) return;
    menu.setAttribute('data-abierto', 'false');
    document.body.classList.remove('menu-abierto');
    if (boton) boton.setAttribute('aria-expanded', 'false');
  }

  if (boton && menu) {
    // escalona la entrada de cada ítem del menú
    Array.prototype.forEach.call(menu.querySelectorAll('.menu__lista a'), function (a, i) {
      a.style.setProperty('--d', (60 + i * 55) + 'ms');
    });

    boton.addEventListener('click', function () {
      var abierto = menu.getAttribute('data-abierto') === 'true';
      menu.setAttribute('data-abierto', abierto ? 'false' : 'true');
      document.body.classList.toggle('menu-abierto', !abierto);
      boton.setAttribute('aria-expanded', String(!abierto));
    });

    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) cerrarMenu();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { cerrarMenu(); boton.focus(); return; }

      // Con el menú abierto el foco no debe escaparse al fondo.
      if (e.key !== 'Tab' || menu.getAttribute('data-abierto') !== 'true') return;

      var foco = menu.querySelectorAll('a[href], button');
      if (!foco.length) return;
      var primero = foco[0], ultimo = foco[foco.length - 1];

      if (e.shiftKey && document.activeElement === primero) {
        e.preventDefault(); ultimo.focus();
      } else if (!e.shiftKey && document.activeElement === ultimo) {
        e.preventDefault(); primero.focus();
      } else if (!menu.contains(document.activeElement) && document.activeElement !== boton) {
        e.preventDefault(); primero.focus();
      }
    });
  }

  /* ---------- 2. Cabecera compacta + barra de progreso ---------- */
  var cabecera = document.querySelector('.cabecera');
  var progreso = document.querySelector('.barra-progreso');
  var tick = false;

  function alScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;

    if (cabecera) cabecera.classList.toggle('compacta', y > 24);

    if (progreso) {
      var alto = document.documentElement.scrollHeight - window.innerHeight;
      var p = alto > 0 ? Math.min(y / alto, 1) : 0;
      progreso.style.transform = 'scaleX(' + p + ')';
    }

    if (typeof window.barrerRevelables === 'function') window.barrerRevelables();
    if (typeof window.pintarCta === 'function') window.pintarCta();
    tick = false;
  }

  window.addEventListener('scroll', function () {
    if (!tick) { tick = true; window.requestAnimationFrame(alScroll); }
  }, { passive: true });
  alScroll();

  /* ---------- 3. Revelado al entrar en pantalla ---------- */
  var pendientes = Array.prototype.slice.call(document.querySelectorAll('.rv, .rv--esc'));

  function revelar(el) {
    el.classList.add('visible');
    var i = pendientes.indexOf(el);
    if (i > -1) pendientes.splice(i, 1);
  }

  if (reduce || !('IntersectionObserver' in window)) {
    pendientes.slice().forEach(revelar);
  } else {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { revelar(e.target); obs.unobserve(e.target); }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -6% 0px' });

    pendientes.forEach(function (el) { obs.observe(el); });

    // Red de seguridad: con un scroll muy rápido el observador puede no
    // alcanzar a disparar y la sección quedaría invisible. En cada cuadro
    // revelamos lo que ya entró en pantalla.
    window.barrerRevelables = function () {
      if (!pendientes.length) return;
      var alto = window.innerHeight;
      pendientes.slice().forEach(function (el) {
        var r = el.getBoundingClientRect();
        // basta con que ya haya entrado en pantalla alguna vez: si el
        // usuario pasó de largo, la sección debe quedar visible igual.
        if (r.top < alto * 0.94) { revelar(el); obs.unobserve(el); }
      });
    };
  }

  /* ---------- 4. Contador de la cifra "+10" ---------- */
  var contadores = document.querySelectorAll('[data-contador]');
  if (contadores.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(contadores, function (el) {
        el.textContent = (el.dataset.prefijo || '') + el.dataset.contador;
      });
    } else {
      var obsNum = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (e) {
          if (!e.isIntersecting) return;
          var el = e.target;
          var fin = parseInt(el.dataset.contador, 10) || 0;
          var pre = el.dataset.prefijo || '';
          var t0 = null;

          function paso(t) {
            if (t0 === null) t0 = t;
            var p = Math.min((t - t0) / 1100, 1);
            var suave = 1 - Math.pow(1 - p, 3);
            el.textContent = pre + Math.round(fin * suave);
            if (p < 1) window.requestAnimationFrame(paso);
          }
          window.requestAnimationFrame(paso);
          obsNum.unobserve(el);
        });
      }, { threshold: 0.6 });

      Array.prototype.forEach.call(contadores, function (el) { obsNum.observe(el); });
    }
  }

  /* ---------- 5. Acordeón de preguntas frecuentes ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('.faq__boton'), function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq__item');
      var abierto = item.getAttribute('data-abierto') === 'true';

      // acordeón de uno por vez
      Array.prototype.forEach.call(item.parentNode.querySelectorAll('.faq__item'), function (otro) {
        otro.setAttribute('data-abierto', 'false');
        var b = otro.querySelector('.faq__boton');
        if (b) b.setAttribute('aria-expanded', 'false');
      });

      if (!abierto) {
        item.setAttribute('data-abierto', 'true');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ---------- 6. CTA fija de WhatsApp ---------- */
  var ctaFija = document.querySelector('.cta-fija');
  var ctasHero = document.querySelector('[data-ctas-hero]');

  if (ctaFija) {
    var pie = document.querySelector('.pie');

    // Se muestra sólo cuando ya pasaron los botones del hero, todavía no
    // llegamos al pie (que lleva el crédito de AS BIT) y el menú está cerrado.
    // Se calcula en el scroll y no con IntersectionObserver para que el estado
    // sea siempre coherente, incluso tras un salto de scroll o un resize.
    window.pintarCta = function () {
      var alto = window.innerHeight;
      var pasoHero = ctasHero
        ? ctasHero.getBoundingClientRect().bottom < 0
        : window.scrollY > 520;
      var enPie = pie ? pie.getBoundingClientRect().top < alto - 40 : false;
      var v = pasoHero && !enPie && !document.body.classList.contains('menu-abierto');

      ctaFija.setAttribute('data-visible', v ? 'true' : 'false');
      ctaFija.setAttribute('aria-hidden', v ? 'false' : 'true');
    };

    window.addEventListener('resize', window.pintarCta, { passive: true });
    if (boton) boton.addEventListener('click', function () {
      window.setTimeout(window.pintarCta, 0);
    });
    window.pintarCta();
  }

  /* ---------- 7. Marquesina: duplica el contenido para el bucle ---------- */
  var pista = document.querySelector('.marquesina__pista');
  if (pista && !reduce) {
    var originales = pista.children.length;
    pista.innerHTML += pista.innerHTML;
    Array.prototype.forEach.call(pista.children, function (el, i) {
      if (i < originales) return;
      // Los clones son decorativos: se ocultan al lector de pantalla Y se
      // sacan del orden de tabulación. Un elemento aria-hidden que todavía
      // recibe foco es una violación de WCAG.
      el.setAttribute('aria-hidden', 'true');
      el.setAttribute('tabindex', '-1');
    });
  }

  /* ---------- 8. Formulario que abre WhatsApp ---------- */
  var form = document.getElementById('form-consulta');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var nombre = (form.nombre.value || '').trim();
      var telefono = (form.telefono.value || '').trim();
      var caso = (form.caso.value || '').trim();

      var texto = 'Hola Blas, soy ' + (nombre || 'una persona interesada') + '.';
      if (telefono) texto += ' Mi teléfono es ' + telefono + '.';
      if (caso) texto += ' Te cuento mi caso: ' + caso;

      var url = 'https://wa.me/595984750151?text=' + encodeURIComponent(texto);
      window.open(url, '_blank', 'noopener');

      var ok = document.getElementById('form-ok');
      if (ok) ok.setAttribute('data-visible', 'true');
    });
  }

  /* ---------- 9. Conversiones a Google Analytics ---------- */
  // Cada clic a WhatsApp se reporta como evento para poder medir
  // conversiones en GA4 y vincularlas con Google Ads / Search Console.
  document.addEventListener('click', function (e) {
    if (typeof window.gtag !== 'function') return;

    var wa = e.target.closest('[data-wa]');
    if (wa) {
      window.gtag('event', 'contacto_whatsapp', {
        ubicacion: wa.getAttribute('data-wa'),
        pagina: document.title
      });
      return;
    }

    // Reseñas de Google: separar quien va a escribir una de quien va a leerlas.
    var ev = e.target.closest('[data-ev]');
    if (ev) {
      window.gtag('event', ev.getAttribute('data-ev'), { pagina: document.title });
    }
  });

  /* ---------- 10. Año en el pie ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-anio]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
