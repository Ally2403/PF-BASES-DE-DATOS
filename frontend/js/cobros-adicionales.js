(function () {
  const COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  function $(id) {
    return document.getElementById(id);
  }

  function esc(t) {
    const d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  /* ── Catálogos ─────────────────────────── */
  let todosConceptos = [];
  let estudiantesLista = [];

  function getFiltradosEstudiantes() {
    const inp = $("ca-filtro-est");
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
    const tb = $("ca-tbl-est");
    const lbl = $("ca-lbl-est");
    if (!tb) return;

    const list = getFiltradosEstudiantes();
    tb.innerHTML = "";
    const currentSel = Number($("ca-est").value);

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
          esc(e.carnet) +
          "</td><td>" +
          esc(e.nombre) +
          "</td><td>" +
          esc(e.apellido) +
          "</td><td>" +
          esc(e.correo) +
          "</td><td>" +
          esc(e.nombre_programa) +
          "</td>";
        tr.onclick = function () {
          $("ca-est").value = id;
          if (lbl) lbl.textContent = "Seleccionado: " + e.nombre + " " + e.apellido + " (" + e.carnet + ")";
          renderTablaEstudiantes();
          onSeleccionChange();
        };
        tb.appendChild(tr);
      });
    }
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
    const s = $("ca-per");
    s.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija período —";
    s.appendChild(ph);
    list.forEach(function (p) {
      var o = document.createElement("option");
      o.value = p.id_periodo;
      o.textContent = p.nombre_periodo;
      s.appendChild(o);
    });
  }

  async function cargarConceptos() {
    try {
      const raw = await api.getCodigosDetalle();
      const list = Array.isArray(raw) ? raw : (raw.data || []);
      // Filter only COBROs that make sense as ad-hoc additions (exclude the base ones PMAT/PCRE)
      todosConceptos = list.filter(function (c) {
        return c.grupo === "COBRO" && c.codigo_detalle !== "PMAT" && c.codigo_detalle !== "PCRE";
      });

      const s = $("ca-codigo");
      s.innerHTML = "";
      var ph = document.createElement("option");
      ph.value = "";
      ph.textContent = "— Elija concepto —";
      s.appendChild(ph);

      todosConceptos.forEach(function (c) {
        var o = document.createElement("option");
        o.value = c.codigo_detalle;
        o.textContent = c.codigo_detalle + " — " + c.descripcion;
        s.appendChild(o);
      });
    } catch (e) {
      console.error("Error al cargar conceptos:", e);
    }
  }

  function onConceptoChange() {
    const cod = $("ca-codigo").value;
    if (!cod) return;
    const c = todosConceptos.find(function (x) { return x.codigo_detalle === cod; });
    if (c) {
      if (c.valor_defecto !== null && c.valor_defecto !== undefined) {
        $("ca-valor").value = c.valor_defecto;
      } else {
        $("ca-valor").value = "";
      }
      if ($("ca-desc")) {
        $("ca-desc").value = c.descripcion;
      }
    } else {
      $("ca-valor").value = "";
      if ($("ca-desc")) $("ca-desc").value = "";
    }
  }

  /* ── Selección ─────────────────────────── */
  function onSeleccionChange() {
    const idE = $("ca-est").value;
    const idP = $("ca-per").value;
    if (!idE || !idP) {
      $("ca-form-card").hidden = true;
      $("ca-historial").hidden = true;
      return;
    }
    $("ca-form-card").hidden = false;
    $("ca-err").hidden = true;
    $("form-ca").reset();
    $("ca-codigo").value = "";
    cargarHistorial();
  }

  /* ── Historial ─────────────────────────── */
  async function cargarHistorial() {
    const idE = $("ca-est").value;
    const idP = $("ca-per").value;
    if (!idE || !idP) return;

    const movs = await api.getCuentaCorriente({ estudiante: idE, periodo: idP });
    const cobros = (Array.isArray(movs) ? movs : []).filter(function (m) {
      return m.grupo === "COBRO";
    });

    const tb = $("ca-tbl");
    tb.innerHTML = "";
    let total = 0;
    cobros.forEach(function (m) {
      total += Number(m.debito || 0);
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" + esc(m.fecha) +
        "</td><td><code>" + esc(m.codigo_detalle) +
        "</code></td><td>" + esc(m.descripcion_movimiento) +
        "</td><td class='numeric'>" + COP.format(m.debito || 0) +
        "</td>";
      tb.appendChild(tr);
    });
    $("ca-total").textContent = "Total cobros: " + COP.format(total);
    $("ca-historial").hidden = cobros.length === 0;
  }

  /* ── Submit ────────────────────────────── */
  async function enviarCobro(ev) {
    ev.preventDefault();
    $("ca-err").hidden = true;

    const idEst = Number($("ca-est").value);
    const idPer = Number($("ca-per").value);
    const codigo = $("ca-codigo").value;
    const valor = Number($("ca-valor").value);
    const desc = $("ca-desc").value.trim();

    if (!idEst || !idPer) {
      $("ca-err").textContent = "Seleccione estudiante y período.";
      $("ca-err").hidden = false;
      return;
    }
    if (!codigo) {
      $("ca-err").textContent = "Seleccione un concepto de cobro.";
      $("ca-err").hidden = false;
      return;
    }
    if (!valor || valor <= 0) {
      $("ca-err").textContent = "Ingrese un valor válido mayor a 0.";
      $("ca-err").hidden = false;
      return;
    }

    try {
      await api.postCobroAdicional({
        id_volante: null,
        id_estudiante: idEst,
        id_periodo: idPer,
        codigo_detalle: codigo,
        valor: valor,
        descripcion: desc,
      });
      auth.showToast(
        "Cobro " + codigo + " por " + COP.format(valor) + " agregado a la cuenta corriente."
      );
      $("form-ca").reset();
      $("ca-codigo").value = "";
      $("ca-valor").value = "";
      if ($("ca-desc")) $("ca-desc").value = "";
      await cargarHistorial();
    } catch (e) {
      $("ca-err").textContent = e.message;
      $("ca-err").hidden = false;
    }
  }

  /* ── Init ──────────────────────────────── */
  document.addEventListener("DOMContentLoaded", async function () {
    await cargarEstudiantes();
    await cargarPeriodos();
    await cargarConceptos();
    $("ca-est").value = "";
    $("ca-per").value = "";

    $("ca-filtro-est").addEventListener("input", renderTablaEstudiantes);
    $("ca-per").addEventListener("change", onSeleccionChange);
    $("ca-codigo").addEventListener("change", onConceptoChange);
    $("form-ca").addEventListener("submit", enviarCobro);
  });
})();
