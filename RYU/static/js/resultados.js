(function () {
  const cfg = window.RYU_RESULTS || { labels: [], values: [] };
  const labels = Array.isArray(cfg.labels) ? cfg.labels : [];
  const values = Array.isArray(cfg.values) ? cfg.values : [];

  const canvas = document.getElementById("pieCanvas");
  const ctx = canvas ? canvas.getContext("2d") : null;
  const legend = document.getElementById("legend");
  const note = document.getElementById("chartNote");
  const totalEl = document.getElementById("totalValue");

  if (!canvas || !ctx || !legend) return;

  function setupHiDPI(c) {
    const dpr = window.devicePixelRatio || 1;
    const rect = c.getBoundingClientRect();
    const w = Math.round(rect.width);
    const h = Math.round(rect.height);
    c.width = Math.round(w * dpr);
    c.height = Math.round(h * dpr);
    const context = c.getContext("2d");
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { w, h, context };
  }

  canvas.style.width = "440px";
  canvas.style.height = "440px";

  const { w, h, context } = setupHiDPI(canvas);
  const cx = w / 2;
  const cy = h / 2;
  const radius = Math.min(cx, cy) - 10;
  const innerRadius = Math.round(radius * 0.55);

  const total = values.reduce((a, b) => a + (Number(b) || 0), 0);
  if (totalEl) totalEl.textContent = total ? String(total) : "0";

  if (!total) {
    legend.innerHTML = "";
    if (note) {
      note.style.display = "block";
      note.textContent = "No hay puntajes para graficar.";
    }
    context.clearRect(0, 0, w, h);
    context.font = "16px Roboto, Arial";
    context.fillStyle = "#4B5563";
    context.fillText("No hay puntajes para graficar.", 20, 30);
    return;
  }

  function colorForIndex(i, n) {
    const hue = Math.round((360 * i) / Math.max(n, 1));
    return `hsl(${hue}, 70%, 55%)`;
  }

  const slices = values.map((val, i) => {
    const v = Number(val) || 0;
    const fraction = v / total;
    return {
      label: labels[i] ? labels[i].replace(/^BP2\s*-\s*/, '').replace(/^\w/, c => c.toUpperCase()) : `Carrera ${i + 1}`,
      value: v,
      fraction,
      color: colorForIndex(i, values.length),
    };
  });

  // Legend
  legend.innerHTML = "";
  slices.forEach((s) => {
    const pct = (s.fraction * 100);
    const item = document.createElement("div");
    item.className = "legend-item";
    item.innerHTML = `
      <div class="legend-left">
        <span class="legend-swatch" style="background:${s.color}"></span>
        <span class="legend-name" title="${escapeHtml(s.label)}">${escapeHtml(s.label)}</span>
      </div>
      <div class="legend-right">${s.value} (${pct.toFixed(1)}%)</div>
    `;
    legend.appendChild(item);
  });

  const duration = 900;
  const startTime = performance.now();

  function draw(progress01) {
    context.clearRect(0, 0, w, h);

    const maxAngle = (Math.PI * 2) * progress01;
    let startAngle = -Math.PI / 2;

    // Guardamos info de ángulos para luego poner % encima
    const drawnSlices = [];

    for (let i = 0; i < slices.length; i++) {
      const s = slices[i];
      if (s.value <= 0) continue;

      const sliceAngle = s.fraction * Math.PI * 2;
      const endAngle = startAngle + sliceAngle;

      const drawEnd = Math.min(endAngle, -Math.PI / 2 + maxAngle);
      if (drawEnd <= startAngle) break;

      // Dibuja porción
      context.beginPath();
      context.moveTo(cx, cy);
      context.arc(cx, cy, radius, startAngle, drawEnd);
      context.closePath();
      context.fillStyle = s.color;
      context.fill();

      context.strokeStyle = "rgba(255,255,255,.9)";
      context.lineWidth = 2;
      context.stroke();

      // Si esta porción ya terminó de dibujarse (para no poner % mientras crece)
      const fullyDrawn = (drawEnd >= endAngle - 1e-6);
      if (fullyDrawn) {
        drawnSlices.push({ ...s, startAngle, endAngle });
      }

      startAngle = endAngle;
    }

    // Hueco donut
    context.save();
    context.globalCompositeOperation = "destination-out";
    context.beginPath();
    context.arc(cx, cy, innerRadius, 0, Math.PI * 2);
    context.fill();
    context.restore();

    // Borde del donut
    context.beginPath();
    context.arc(cx, cy, innerRadius, 0, Math.PI * 2);
    context.strokeStyle = "rgba(31,41,55,.10)";
    context.lineWidth = 1;
    context.stroke();

    // ✅ Porcentajes encima (solo cuando ya se dibujó la porción)
    // Regla: solo mostrar si >= 6% para evitar amontonamiento
    context.font = "700 14px Montserrat, Roboto, Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";

    drawnSlices.forEach((s) => {
      const pct = s.fraction * 100;
      if (pct < 6) return;

      const mid = (s.startAngle + s.endAngle) / 2;
      const rLabel = (innerRadius + radius) / 2; // mitad del grosor
      const x = cx + Math.cos(mid) * rLabel;
      const y = cy + Math.sin(mid) * rLabel;

      // Texto en color de la porción, con contorno blanco para legibilidad
      const text = `${pct.toFixed(1)}%`;

      context.lineWidth = 4;
      context.strokeStyle = "rgba(255,255,255,.95)";
      context.strokeText(text, x, y);

      context.fillStyle = s.color;
      context.fillText(text, x, y);
    });
  }

  function animate(now) {
    const t = Math.min(1, (now - startTime) / duration);
    const eased = 1 - Math.pow(1 - t, 3);
    draw(eased);
    if (t < 1) requestAnimationFrame(animate);
    else draw(1);
  }

  requestAnimationFrame(animate);

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
})();
