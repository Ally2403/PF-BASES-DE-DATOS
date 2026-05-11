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
    var nom = byId("per-nombre");
    var ini = byId("per-inicio");
    var fin = byId("per-fin");
    if (id) id.value = "";
    if (nom) nom.value = "";
    if (ini) ini.value = "";
    if (fin) fin.value = "";
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
      toast(e.message || "Error al cargar periodos", "error");
    }
  }

  function abrirModalNuevo() {
    limpiarModal();
    var title = byId("per-modal-title");
    if (title) title.textContent = "Nuevo periodo";
    setModalOpen(true);
  }

  async function abrirModalEditar(id) {
    try {
      var list = normalizarListaPeriodos(await api.getPeriodos({ id_periodo: id }));
      if (!list.length) throw new Error("Periodo no encontrado");
      var p = list[0];
      var hid = byId("per-id");
      var nom = byId("per-nombre");
      var ini = byId("per-inicio");
      var fin = byId("per-fin");
      var title = byId("per-modal-title");
      if (hid) hid.value = String(p.id_periodo);
      if (nom) nom.value = p.nombre_periodo || p.nombre || "";
      if (ini) ini.value = p.fecha_inicio || "";
      if (fin) fin.value = p.fecha_fin || "";
      if (title) title.textContent = "Editar periodo";
      setModalOpen(true);
    } catch (e) {
      toast(e.message || "Error al abrir periodo", "error");
    }
  }

  async function guardar(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var hid = byId("per-id");
    var nom = byId("per-nombre");
    var ini = byId("per-inicio");
    var fin = byId("per-fin");
    var id = hid && hid.value ? Number(hid.value) : 0;
    var body = {
      nombre_periodo: nom ? nom.value.trim() : "",
      fecha_inicio: ini ? ini.value : "",
      fecha_fin: fin ? fin.value : "",
    };
    if (!body.nombre_periodo || !body.fecha_inicio || !body.fecha_fin) {
      toast("Complete nombre, inicio y fin.", "error");
      return;
    }
    try {
      if (typeof api.postPeriodo !== "function" || typeof api.putPeriodo !== "function") {
        toast("api.postPeriodo / putPeriodo no están disponibles.", "error");
        return;
      }
      if (!id) {
        await api.postPeriodo(body);
        toast("Periodo guardado", "success");
      } else {
        await api.putPeriodo(id, body);
        toast("Periodo actualizado", "success");
      }
      setModalOpen(false);
      limpiarModal();
      await recargar();
    } catch (e) {
      toast(e.message || "Error al guardar", "error");
    }
  }

  async function eliminar(id) {
    if (!window.confirm("¿Seguro que desea eliminar?")) return;
    try {
      await api.deletePeriodo(id);
      toast("Periodo eliminado", "success");
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
