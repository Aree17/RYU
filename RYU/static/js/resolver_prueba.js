(function () {
  // Variables desde Django
  const cfg = window.RYU_TEST || { indiceInicial: 0, urlAbandonar: "" };

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrfToken = getCookie("csrftoken");

  let actual = Number(cfg.indiceInicial || 0);

  const preguntas = document.querySelectorAll(".pregunta");
  const botones = document.querySelectorAll(".side-btn");
  const inputIndice = document.getElementById("indice_actual");
  const errorBox = document.getElementById("error-msg");

  function setError(msg) {
    if (!msg) {
      errorBox.style.display = "none";
      errorBox.textContent = "";
      return;
    }
    errorBox.style.display = "block";
    errorBox.textContent = msg;
  }

  function estaRespondida(index) {
    const radios = preguntas[index].querySelectorAll('input[type="radio"]');
    return Array.from(radios).some(r => r.checked);
  }

  function actualizarMarcadoRespondidas() {
    for (let i = 0; i < preguntas.length; i++) {
      if (!botones[i]) continue;
      if (estaRespondida(i)) botones[i].classList.add("respondida");
      else botones[i].classList.remove("respondida");
    }
  }

  function mostrarPregunta(index) {
    preguntas.forEach(p => p.classList.remove("activa"));
    botones.forEach(b => b.classList.remove("activa"));

    actual = index;

    preguntas[actual].classList.add("activa");
    if (botones[actual]) botones[actual].classList.add("activa");

    if (inputIndice) inputIndice.value = actual;

    setError(null);
    actualizarMarcadoRespondidas();
  }

  // Exponer funciones para los onclick del template
  window.siguiente = function () {
    if (!estaRespondida(actual)) {
      setError("Responde esta pregunta antes de continuar.");
      return;
    }
    if (actual < preguntas.length - 1) mostrarPregunta(actual + 1);
  };

  window.anterior = function () {
    if (actual > 0) mostrarPregunta(actual - 1);
  };

  window.irAPregunta = function (index) {
    mostrarPregunta(index);
  };

  document.addEventListener("change", (e) => {
    if (e.target.matches('input[type="radio"]')) {
      actualizarMarcadoRespondidas();
      setError(null);
    }
  });

  if (preguntas.length > 0) {
    if (actual < 0 || actual >= preguntas.length) actual = 0;
    mostrarPregunta(actual);
  }

  let enviado = false;
  const form = document.getElementById("form-prueba");

  if (form) {
    form.addEventListener("submit", (e) => {
      for (let i = 0; i < preguntas.length; i++) {
        if (!estaRespondida(i)) {
          e.preventDefault();
          mostrarPregunta(i);
          setError("Debes responder todas las preguntas antes de enviar.");
          return;
        }
      }
      enviado = true;
    });
  }

  // Modal de salida
  const modal = document.getElementById("modal-salida");
  const btnQuedarme = document.getElementById("btn-quedarme");
  const btnSalir = document.getElementById("btn-salir");
  let destinoPendiente = null;

  const urlAbandonar = String(cfg.urlAbandonar || "");

  function abrirModal(destino) {
    if (enviado) { window.location.href = destino; return; }
    destinoPendiente = destino;
    if (modal) modal.style.display = "flex";
  }

  function cerrarModal() {
    if (modal) modal.style.display = "none";
    destinoPendiente = null;
  }

  async function abandonarYSalir() {
    try {
      await fetch(urlAbandonar, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken
        },
        body: "",
        keepalive: true
      });
    } catch (e) {}

    if (destinoPendiente) window.location.href = destinoPendiente;
  }

  if (btnQuedarme) btnQuedarme.addEventListener("click", cerrarModal);
  if (btnSalir) btnSalir.addEventListener("click", abandonarYSalir);

  document.querySelectorAll("a.nav-salida").forEach(a => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      abrirModal(a.href);
    });
  });

  // Si cierran pestaña / navegan fuera
  window.addEventListener("beforeunload", (e) => {
    if (enviado || !urlAbandonar) return;
    e.preventDefault();
    e.returnValue = "";
    try {
      navigator.sendBeacon(urlAbandonar, new Blob([], { type: "application/x-www-form-urlencoded" }));
    } catch (err) {}
  });

  window.addEventListener("pagehide", () => {
    if (enviado || !urlAbandonar) return;
    try {
      navigator.sendBeacon(urlAbandonar, new Blob([], { type: "application/x-www-form-urlencoded" }));
    } catch (err) {}
  });

})();
