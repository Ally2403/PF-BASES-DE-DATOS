(function () {
  const COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  function $(id) {
    return document.getElementById(id);
  }

  let estudiantesLista = [];

  function getFiltradosEstudiantes() {
    const inp = $("pg-filtro-est");
    const q = inp && inp.value ? inp.value.trim().toLowerCase() : "";
    const base = Array.isArray(estudiantesLista) ? estudiantesLista : [];
    if (!q) return base.slice();
    return base.filter(function (e) {
      const nom = String(e.nombre || "").toLowerCase();
      const ape = String(e.apellido || "").toLowerCase();
      const full = nom + " " + ape;
      const prog = String(e.nombre_programa || "").toLowerCase();
      return (
        nom.includes(q) ||
        ape.includes(q) ||
        full.includes(q) ||
        String(e.carnet || "").toLowerCase().includes(q) ||
        String(e.correo || "").toLowerCase().includes(q) ||
        prog.includes(q)
      );
    });
  }

  function renderTablaEstudiantes() {
    const tb = $("pg-tbl-est");
    const lbl = $("pg-lbl-est");
    if (!tb) return;

    const list = getFiltradosEstudiantes();
    tb.innerHTML = "";
    const currentSel = Number($("pg-est").value);

    if (!list.length) {
      tb.innerHTML = '<tr><td colspan="5" style="color:var(--text-muted)">Sin coincidencias.</td></tr>';
    } else {
      list.forEach(function (e) {
        const id = Number(e.id_estudiante);
        const tr = document.createElement("tr");
        tr.dataset.idEstudiante = String(id);
        if (currentSel && id === currentSel) tr.classList.add("is-selected");
        tr.innerHTML =
          "<td>" +
          escapeHtml(e.carnet) +
          "</td><td>" +
          escapeHtml(e.nombre) +
          "</td><td>" +
          escapeHtml(e.apellido) +
          "</td><td>" +
          escapeHtml(e.correo) +
          "</td><td>" +
          escapeHtml(e.nombre_programa) +
          "</td>";
        tr.onclick = function () {
          $("pg-est").value = id;
          if (lbl) lbl.textContent = "Seleccionado: " + e.nombre + " " + e.apellido + " (" + e.carnet + ")";
          renderTablaEstudiantes();
          cargarConceptos();
        };
        tb.appendChild(tr);
      });
    }
  }

  function escapeHtml(t) {
    const d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  async function cargarEstudiantes() {
    const raw = await api.getEstudiantes({});
    estudiantesLista =
      typeof api.normalizarListaEstudiantes === "function"
        ? api.normalizarListaEstudiantes(raw)
        : Array.isArray(raw)
          ? raw
          : [];
    renderTablaEstudiantes();
  }

  async function cargarPeriodos() {
    let list = await api.getPeriodos();
    list = Array.isArray(list) ? list : [];
    if (typeof api.sortPeriodosRecientesPrimero === "function") {
      list = api.sortPeriodosRecientesPrimero(list.slice());
    }
    const s = $("pg-per");
    s.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Seleccionar período —";
    s.appendChild(ph);
    list.forEach(function (p) {
      const o = document.createElement("option");
      o.value = p.id_periodo;
      o.textContent = p.nombre_periodo;
      s.appendChild(o);
    });
  }

  async function cargarCodigosPago() {
    const s = $("pg-cod");
    s.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija tipo de pago —";
    s.appendChild(ph);
    try {
      const all = await api.getCodigosDetalle();
      const list = all.filter((c) => c.grupo === "PAGO");
      list.forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c.codigo_detalle;
        opt.textContent = c.descripcion + " (" + c.codigo_detalle + ")";
        s.appendChild(opt);
      });
      if (list.some((c) => c.codigo_detalle === "MPAG")) {
        s.value = "MPAG";
      }
    } catch (e) {
      console.error(e);
    }
  }

  document.addEventListener("DOMContentLoaded", async function () {
    await cargarEstudiantes();
    await cargarPeriodos();
    await cargarCodigosPago();
    $("pg-est").value = "";
    $("pg-per").value = "";

    $("pg-filtro-est").addEventListener("input", renderTablaEstudiantes);

    $("form-pago").addEventListener("submit", async function (ev) {
      ev.preventDefault();
      $("pg-err").hidden = true;
      const est = $("pg-est").value;
      const per = $("pg-per").value;
      if (!est || !per) {
        $("pg-err").textContent = "Seleccione estudiante y período.";
        $("pg-err").hidden = false;
        return;
      }
      const cod = $("pg-cod").value;
      const val = Number($("pg-val").value);
      const medio = $("pg-med").value;
      const ref = $("pg-ref").value.trim();

      if (!cod) {
        $("pg-err").textContent = "Seleccione un concepto de pago.";
        $("pg-err").hidden = false;
        return;
      }
      if (!medio) {
        $("pg-err").textContent = "Seleccione el medio de pago.";
        $("pg-err").hidden = false;
        return;
      }
      if (!val || val <= 0) {
        $("pg-err").textContent = "Valor inválido.";
        $("pg-err").hidden = false;
        return;
      }

      try {
        await api.postPago({
          id_estudiante: Number(est),
          id_periodo: Number(per),
          codigo_detalle: cod,
          medio_pago: medio,
          referencia: ref,
          valor_pagado: val,
        });
        auth.showToast("Pago registrado con éxito.");
        ev.target.reset();
        $("pg-est").value = "";
        $("pg-per").value = "";
        $("pg-med").value = "";
        await cargarCodigosPago();
      } catch (e) {
        $("pg-err").textContent = e.message;
        $("pg-err").hidden = false;
      }
    });
  });
})();
