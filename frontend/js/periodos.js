/**
 * Periodos: tabla + búsqueda en vivo + modal crear/editar.
 * Arranque según readyState para no perder DOMContentLoaded si el script carga tarde.
 */
(function () {
  function byId(id) {
    return document.getElementById(id);
  }

  function esc(t) {
    var d = document.createElement("div");
    var s = t === null || t === undefined ? "" : String(t);
    d.textContent = s;
    return d.innerHTML;
  }

  /** Acepta array o envoltorios típicos del backend */
  function normalizarListaPeriodos(raw) {
    if (Array.isArray(raw)) return raw;
    if (raw && Array.isArray(raw.data)) return raw.data;
    if (raw && Array.isArray(raw.periodos)) return raw.periodos;
    if (raw && Array.isArray(raw.items)) return raw.items;
    if (raw && Array.isArray(raw.results)) return raw.results;
    return [];
  }

  function closestButton(el) {
    while (el && el !== document.body) {
      if (el.tagName === "BUTTON") return el;
      el = el.parentNode;
    }
    return null;
  }

  var periodosCache = [];

  function setModalOpen(open) {
    var modal = byId("per-modal");
    if (!modal) return;
    if (open) {
      modal.classList.add("open");
    } else {
      modal.classList.remove("open");
    }
    modal.setAttribute("aria-hidden", open ? "false" : "true");
  }

  function limpiarModal() {
    var id = byId("per-id");
    var anio = byId("per-anio");
    var sem = byId("per-semestre");
    var ini = byId("per-inicio");
    var fin = byId("per-fin");
    var previewRow = byId("per-preview-row");
    var preview = byId("per-nombre-preview");
    var rangoInfo = byId("per-rango-info");
    if (id) id.value = "";
    if (anio) anio.value = "";
    if (sem) sem.value = "";
    if (ini) { ini.value = ""; ini.removeAttribute("min"); ini.removeAttribute("max"); }
    if (fin) { fin.value = ""; fin.removeAttribute("min"); fin.removeAttribute("max"); }
    if (previewRow) previewRow.hidden = true;
    if (preview) preview.textContent = "";
    if (rangoInfo) { rangoInfo.style.display = "none"; rangoInfo.textContent = ""; }
  }

  function actualizarPeriodo() {
    var anio = byId("per-anio");
    var sem = byId("per-semestre");
    var ini = byId("per-inicio");
    var fin = byId("per-fin");
    var previewRow = byId("per-preview-row");
    var preview = byId("per-nombre-preview");
    var rangoInfo = byId("per-rango-info");
    var year = anio ? parseInt(anio.value, 10) : NaN;
    var semVal = sem ? sem.value : "";

    if (!year || isNaN(year) || !semVal) {
      if (previewRow) previewRow.hidden = true;
      if (preview) preview.textContent = "";
      if (rangoInfo) rangoInfo.style.display = "none";
      if (ini) { ini.removeAttribute("min"); ini.removeAttribute("max"); }
      if (fin) { fin.removeAttribute("min"); fin.removeAttribute("max"); }
      return;
    }

    if (preview) preview.textContent = year + "-" + semVal;
    if (previewRow) previewRow.hidden = false;

    var minDate, maxDate, msg;
    if (semVal === "10") {
      minDate = year + "-01-01";
      maxDate = year + "-06-30";
      msg = "Primer semestre " + year + ": las fechas de inicio y fin deben estar entre el 1 de enero y el 30 de junio de " + year + ".";
    } else {
      minDate = year + "-07-01";
      maxDate = year + "-12-31";
      msg = "Segundo semestre " + year + ": las fechas de inicio y fin deben estar entre el 1 de julio y el 31 de diciembre de " + year + ".";
    }

    if (ini) { ini.setAttribute("min", minDate); ini.setAttribute("max", maxDate); }
    if (fin) { fin.setAttribute("min", minDate); fin.setAttribute("max", maxDate); }
    if (rangoInfo) { rangoInfo.textContent = "Rango válido: " + msg; rangoInfo.style.display = ""; }
  }

  function getFiltrados() {
    var inp = byId("filtro-per");
    var q = inp && inp.value ? inp.value.trim().toLowerCase() : "";
    if (!q) return periodosCache.slice();
    return periodosCache.filter(function (p) {
      var n = String(p.nombre_periodo || p.nombre || "").toLowerCase();
      return n.indexOf(q) !== -1;
    });
  }

  function renderTabla() {
    var tb = byId("tbl-periodos");
    var lbl = byId("lbl-total-per");
    if (!tb) return;
    var rows = getFiltrados();
    tb.innerHTML = "";
    rows.forEach(function (p) {
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        esc(p.nombre_periodo || p.nombre || "") +
        "</td><td>" +
        esc(p.fecha_inicio) +
        "</td><td>" +
        esc(p.fecha_fin) +
        "</td><td>" +
        '<div class="btn-row">' +
        '<button type="button" class="btn btn-secondary btn-edit-per" data-id="' +
        esc(p.id_periodo) +
        '">Editar</button>' +
        '<button type="button" class="btn btn-danger btn-del-per" data-id="' +
        esc(p.id_periodo) +
        '">Eliminar</button>' +
        "</div>" +
        "</td>";
      tb.appendChild(tr);
    });
    if (lbl) {
      lbl.textContent =
        "Mostrando " + rows.length + " de " + periodosCache.length + " registros.";
    }
  }

  function toast(msg, kind) {
    if (window.auth && typeof auth.showToast === "function") {
      auth.showToast(msg, kind || "error");
    } else {
      window.alert(msg);
    }
  }

  async function recargar() {
    try {
      if (!window.api || typeof api.getPeriodos !== "function") {
        toast("api.getPeriodos no está disponible. Revise que api.js cargue bien.", "error");
        return;
      }
      var raw = await api.getPeriodos();
      periodosCache = normalizarListaPeriodos(raw);
      renderTabla();
    } catch (e) {
      toast(e.message || "Error al cargar períodos", "error");
    }
  }

  function abrirModalNuevo() {
    limpiarModal();
    var title = byId("per-modal-title");
    if (title) title.textContent = "Nuevo período";
    setModalOpen(true);
  }

  async function abrirModalEditar(id) {
    try {
      var list = normalizarListaPeriodos(await api.getPeriodos({ id_periodo: id }));
      if (!list.length) throw new Error("Período no encontrado");
      var p = list[0];
      var hid = byId("per-id");
      var anio = byId("per-anio");
      var sem = byId("per-semestre");
      var ini = byId("per-inicio");
      var fin = byId("per-fin");
      var title = byId("per-modal-title");
      if (hid) hid.value = String(p.id_periodo);
      var nombre = p.nombre_periodo || p.nombre || "";
      var parts = nombre.split("-");
      if (anio) anio.value = parts[0] || "";
      if (sem) sem.value = (parts[1] === "10" || parts[1] === "30") ? parts[1] : "";
      if (ini) ini.value = p.fecha_inicio || "";
      if (fin) fin.value = p.fecha_fin || "";
      if (title) title.textContent = "Editar período";
      actualizarPeriodo();
      setModalOpen(true);
    } catch (e) {
      toast(e.message || "Error al abrir período", "error");
    }
  }

  async function guardar(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var hid = byId("per-id");
    var anio = byId("per-anio");
    var sem = byId("per-semestre");
    var ini = byId("per-inicio");
    var fin = byId("per-fin");
    var id = hid && hid.value ? Number(hid.value) : 0;

    var year = anio ? parseInt(anio.value, 10) : NaN;
    var semVal = sem ? sem.value : "";

    if (!year || isNaN(year) || year < 2000 || year > 2099) {
      toast("Ingrese un año válido (2000-2099).", "error");
      return;
    }
    if (!semVal) {
      toast("Seleccione el semestre: 10 (primer semestre) o 30 (segundo semestre).", "error");
      return;
    }

    var fechaInicio = ini ? ini.value : "";
    var fechaFin = fin ? fin.value : "";

    if (!fechaInicio && !fechaFin) {
      toast("Debe ingresar la fecha de inicio y la fecha de fin del período.", "error");
      return;
    }
    if (!fechaInicio) {
      toast("Falta la fecha de inicio. Indique el primer día del período.", "error");
      return;
    }
    if (!fechaFin) {
      toast("Falta la fecha de fin. Indique el último día del período.", "error");
      return;
    }
    if (fechaFin <= fechaInicio) {
      toast("La fecha de fin (" + fechaFin + ") debe ser posterior a la fecha de inicio (" + fechaInicio + ").", "error");
      return;
    }

    var minDate, maxDate, labelRango, labelMin, labelMax;
    if (semVal === "10") {
      minDate = year + "-01-01";
      maxDate = year + "-06-30";
      labelRango = "el primer semestre " + year;
      labelMin = "1 de enero de " + year;
      labelMax = "30 de junio de " + year;
    } else {
      minDate = year + "-07-01";
      maxDate = year + "-12-31";
      labelRango = "el segundo semestre " + year;
      labelMin = "1 de julio de " + year;
      labelMax = "31 de diciembre de " + year;
    }
    if (fechaInicio < minDate || fechaInicio > maxDate) {
      toast(
        "La fecha de inicio (" + fechaInicio + ") no corresponde a " + labelRango + ". " +
        "Debe estar entre el " + labelMin + " y el " + labelMax + ".",
        "error"
      );
      return;
    }
    if (fechaFin < minDate || fechaFin > maxDate) {
      toast(
        "La fecha de fin (" + fechaFin + ") no corresponde a " + labelRango + ". " +
        "Debe estar entre el " + labelMin + " y el " + labelMax + ".",
        "error"
      );
      return;
    }

    var body = {
      nombre_periodo: year + "-" + semVal,
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
    };
    try {
      if (typeof api.postPeriodo !== "function" || typeof api.putPeriodo !== "function") {
        toast("api.postPeriodo / putPeriodo no están disponibles.", "error");
        return;
      }
      if (!id) {
        await api.postPeriodo(body);
        toast("Período guardado", "success");
      } else {
        await api.putPeriodo(id, body);
        toast("Período actualizado", "success");
      }
      setModalOpen(false);
      limpiarModal();
      await recargar();
    } catch (e) {
      toast(e.message || "Error al guardar", "error");
    }
  }

  async function eliminar(id) {
    if (!await auth.showConfirm("¿Desea eliminar este período académico? Esta acción no se puede deshacer.")) return;
    if (!await auth.showConfirmCedula(
      "Está a punto de eliminar un período académico.",
      "Si existen volantes de matrícula, movimientos financieros o cobros registrados en este período, la eliminación será bloqueada. De eliminarse, se perderá la referencia temporal de todos los registros asociados."
    )) return;
    try {
      await api.deletePeriodo(id);
      toast("Período eliminado", "success");
      await recargar();
    } catch (e) {
      toast(e.message || "No se pudo eliminar", "error");
    }
  }

  function init() {
    if (window.__periodosPageInited) return;

    var ids = [
      "btn-nuevo-per",
      "filtro-per",
      "form-per-modal",
      "btn-close-per-modal",
      "btn-cancel-per-modal",
      "per-modal",
      "tbl-periodos",
      "lbl-total-per",
      "per-anio",
      "per-semestre",
    ];
    var missing = [];
    for (var i = 0; i < ids.length; i++) {
      if (!byId(ids[i])) missing.push(ids[i]);
    }
    if (missing.length) {
      toast("Faltan elementos en periodos.html: " + missing.join(", "), "error");
      return;
    }

    window.__periodosPageInited = true;

    byId("btn-nuevo-per").addEventListener("click", abrirModalNuevo);
    byId("filtro-per").addEventListener("input", renderTabla);
    byId("form-per-modal").addEventListener("submit", guardar);
    byId("per-anio").addEventListener("input", actualizarPeriodo);
    byId("per-semestre").addEventListener("change", actualizarPeriodo);
    byId("btn-close-per-modal").addEventListener("click", function () {
      setModalOpen(false);
      limpiarModal();
    });
    byId("btn-cancel-per-modal").addEventListener("click", function () {
      setModalOpen(false);
      limpiarModal();
    });
    byId("per-modal").addEventListener("click", function (ev) {
      if (ev.target === byId("per-modal")) {
        setModalOpen(false);
        limpiarModal();
      }
    });
    byId("tbl-periodos").addEventListener("click", function (ev) {
      var btn = ev.target.closest ? ev.target.closest("button") : closestButton(ev.target);
      if (!btn) return;
      var id = Number(btn.getAttribute("data-id"));
      if (!id) return;
      if (btn.classList.contains("btn-edit-per")) abrirModalEditar(id);
      if (btn.classList.contains("btn-del-per")) eliminar(id);
    });

    recargar();
  }

  window.periodosPageReady = init;
})();
