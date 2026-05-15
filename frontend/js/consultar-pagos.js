(function () {
  const $ = (id) => document.getElementById(id);
  const COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
  });

  function formatFecha(raw) {
    if (!raw) return "—";
    // Normaliza separador T o espacio entre fecha y hora
    return String(raw).replace("T", " ").replace(/\.\d+$/, "");
  }

  let todasLasTransacciones = [];

  async function cargarTodo() {
    try {
      todasLasTransacciones = await api.getPagos({});
      renderTabla();
    } catch (e) {
      console.error(e);
      $("tbl-pagos").innerHTML = '<tr><td colspan="7" class="text-center" style="color:red">Error al cargar datos.</td></tr>';
    }
  }

  function renderTabla() {
    const query = $("f-busqueda").value.trim().toLowerCase();

    const filtradas = todasLasTransacciones.filter(t => {
        if (!query) return true;
        return (
            String(t.id_transaccion).toLowerCase().includes(query) ||
            String(t.referencia).toLowerCase().includes(query) ||
            String(t.medio_pago).toLowerCase().includes(query) ||
            String(t.carnet).toLowerCase().includes(query) ||
            String(t.nombre_estudiante).toLowerCase().includes(query) ||
            String(t.concepto_pago).toLowerCase().includes(query)
        );
    });

    const tb = $("tbl-pagos");
    tb.innerHTML = "";

    if (filtradas.length === 0) {
      tb.innerHTML = '<tr><td colspan="7" class="text-center" style="padding: 2rem; color: var(--text-muted)">No hay registros que coincidan con la búsqueda.</td></tr>';
      return;
    }

    filtradas.forEach((t) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${t.id_transaccion}</td>
        <td>${formatFecha(t.fecha_pago)}</td>
        <td><strong>${t.carnet}</strong><br><small>${t.nombre_estudiante}</small></td>
        <td>${t.referencia || "—"}</td>
        <td><span class="badge ${t.medio_pago === 'SIMULADO_ONLINE' ? 'badge-info' : 'badge-success'}">${t.medio_pago}</span></td>
        <td class="numeric">${COP.format(t.valor_pagado)}</td>
        <td class="text-center">
            <button class="btn btn-small btn-ghost" onclick="verDetalle(${t.id_transaccion})">Ver</button>
        </td>
      `;
      tb.appendChild(tr);
    });
  }

  window.verDetalle = function(id) {
    const t = todasLasTransacciones.find(x => x.id_transaccion === id);
    if (!t) return;

    const modal = $("modal-detalle");
    const body = $("det-body");
    
    $("det-titulo").textContent = `Transacción #${t.id_transaccion}`;
    body.innerHTML = `
        <div class="grid grid-2" style="gap: 1rem;">
            <div>
                <label style="color: var(--text-muted); font-size: 0.8rem;">Estudiante</label>
                <div style="font-weight: bold;">${t.nombre_estudiante}</div>
                <div style="font-size: 0.9rem;">${t.carnet}</div>
            </div>
            <div>
                <label style="color: var(--text-muted); font-size: 0.8rem;">Fecha y Hora</label>
                <div>${formatFecha(t.fecha_pago)}</div>
            </div>
            <div>
                <label style="color: var(--text-muted); font-size: 0.8rem;">Medio de Pago</label>
                <div>${t.medio_pago}</div>
            </div>
            <div>
                <label style="color: var(--text-muted); font-size: 0.8rem;">Referencia</label>
                <div>${t.referencia || 'N/A'}</div>
            </div>
            <div style="grid-column: 1 / -1; border-top: 1px dashed var(--border); padding-top: 1rem; margin-top: 0.5rem;">
                <label style="color: var(--text-muted); font-size: 0.8rem;">Valor Total Pagado</label>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-light);">${COP.format(t.valor_pagado)}</div>
            </div>
            <div style="grid-column: 1 / -1; font-size: 0.8rem; color: var(--text-muted);">
                Vinculado al movimiento ID: ${t.id_mov}<br>
                Concepto: ${t.concepto_pago || '—'}
            </div>
        </div>
    `;

    modal.style.display = "flex";
  };

  window.cerrarDetalle = function() {
    $("modal-detalle").style.display = "none";
  };

  $("f-busqueda").addEventListener("input", renderTabla);

  $("btn-limpiar").addEventListener("click", () => {
    $("f-busqueda").value = "";
    renderTabla();
  });

  cargarTodo();
})();
