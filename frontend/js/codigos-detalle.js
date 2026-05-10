/**
 * Códigos de detalle: tabla + búsqueda + modal crear/editar.
 */
(function () {
  function byId(id) {
    return document.getElementById(id);
  }

  function esc(t) {
    var d = document.createElement("div");
    d.textContent = t === null || t === undefined ? "" : String(t);
    return d.innerHTML;
  }

  function normLista(raw) {
    if (Array.isArray(raw)) return raw;
    if (raw && Array.isArray(raw.data)) return raw.data;
    if (raw && Array.isArray(raw.items)) return raw.items;
    return [];
  }

  var cache = [];

  var COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  function toast(msg, kind) {
    if (window.auth && typeof auth.showToast === "function") {
      auth.showToast(msg, kind || "error");
    } else {
      window.alert(msg);
    }
  }

  function setModal(open) {
    var m = byId("cd-modal");
    if (!m) return;
    if (open) m.classList.add("open");
    else m.classList.remove("open");
    m.setAttribute("aria-hidden", open ? "false" : "true");
  }

  function filtrados() {
    var inp = byId("filtro-cod");
    var q = inp && inp.value ? inp.value.trim().toLowerCase() : "";
    if (!q) return cache.slice();
    return cache.filter(function (r) {
      var blob =
        String(r.codigo_detalle || "").toLowerCase() +
        " " +
        String(r.grupo || "").toLowerCase() +
        " " +
        String(r.descripcion || "").toLowerCase();
      return blob.indexOf(q) !== -1;
    });
  }

  function renderTabla() {
    var tb = byId("tbl-codigos");
    var lbl = byId("lbl-total-cod");
    if (!tb) return;
    var rows = filtrados();
    tb.innerHTML = "";
    rows.forEach(function (r) {
      var tr = document.createElement("tr");
      var cod = esc(r.codigo_detalle);
      tr.innerHTML = `
        <td><code>${cod}</code></td>
        <td>${esc(r.grupo)}</td>
        <td>${esc(r.descripcion)}</td>
        <td>${r.valor_defecto ? COP.format(r.valor_defecto) : '<span style="color:var(--text-muted)">N/A</span>'}</td>
        <td>
          <div class="btn-row">
            <button type="button" class="btn btn-secondary btn-edit-cd" data-cod="${cod}">Editar</button>
            <button type="button" class="btn btn-danger btn-del-cd" data-cod="${cod}">Eliminar</button>
          </div>
        </td>
      `;
      tb.appendChild(tr);
    });
    if (lbl) {
      lbl.textContent =
        "Mostrando " + rows.length + " de " + cache.length + " registros.";
    }
  }

  function limpiarModal() {
    byId("cd-form-mode").value = "new";
    byId("cd-codigo").value = "";
    byId("cd-codigo").readOnly = false;
    byId("cd-grupo").value = "COBRO";
    byId("cd-desc").value = "";
    if (byId("cd-valor")) byId("cd-valor").value = "";
  }

  function abrirNuevo() {
    limpiarModal();
    var t = byId("cd-modal-title");
    if (t) t.textContent = "Nuevo código";
    setModal(true);
  }

  function abrirEditar(codRaw) {
    var key = String(codRaw || "").trim().toUpperCase();
    var r = cache.find(function (x) {
      return String(x.codigo_detalle) === key;
    });
    if (!r) {
      toast("Código no encontrado.", "error");
      return;
    }
    byId("cd-form-mode").value = "edit";
    byId("cd-codigo").value = r.codigo_detalle;
    byId("cd-codigo").readOnly = true;
    byId("cd-grupo").value = r.grupo === "PAGO" ? "PAGO" : "COBRO";
    byId("cd-desc").value = r.descripcion || "";
    if (byId("cd-valor")) byId("cd-valor").value = r.valor_defecto || "";
    var t = byId("cd-modal-title");
    if (t) t.textContent = "Editar código";
    setModal(true);
  }

  async function guardar(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var modo = byId("cd-form-mode").value;
    var codIn = String(byId("cd-codigo").value || "")
      .trim()
      .toUpperCase();
    var grupo = byId("cd-grupo").value;
    var desc = String(byId("cd-desc").value || "").trim();
    var valRaw = byId("cd-valor") ? byId("cd-valor").value : "";
    var val = valRaw ? Number(valRaw) : null;
    if (!codIn || !desc) {
      toast("Complete código y descripción.", "error");
      return;
    }
    try {
      if (modo === "new") {
        await api.postCodigoDetalle({
          codigo_detalle: codIn,
          grupo: grupo,
          descripcion: desc,
          valor_defecto: val
        });
        toast("Código creado", "success");
      } else {
        await api.putCodigoDetalle(codIn, {
          grupo: grupo,
          descripcion: desc,
          valor_defecto: val
        });
        toast("Código actualizado", "success");
      }
      setModal(false);
      limpiarModal();
      await recargar();
    } catch (e) {
      toast(e.message || "Error al guardar", "error");
    }
  }

  async function eliminar(codRaw) {
    var key = String(codRaw || "").trim().toUpperCase();
    if (!window.confirm("¿Seguro que desea eliminar?")) return;
    try {
      await api.deleteCodigoDetalle(key);
      toast("Código eliminado", "success");
      await recargar();
    } catch (e) {
      toast(e.message || "No se pudo eliminar", "error");
    }
  }

  async function recargar() {
    try {
      if (typeof api.getCodigosDetalle !== "function") {
        toast("getCodigosDetalle no disponible", "error");
        return;
      }
      var raw = await api.getCodigosDetalle();
      cache = normLista(raw);
      renderTabla();
    } catch (e) {
      toast(e.message || "Error al cargar códigos", "error");
    }
  }

  function onTblClick(ev) {
    var t = ev.target;
    var btn = null;
    if (t && t.closest) btn = t.closest("button");
    else {
      while (t && t !== document.body) {
        if (t.tagName === "BUTTON") {
          btn = t;
          break;
        }
        t = t.parentNode;
      }
    }
    if (!btn) return;
    var cod = btn.getAttribute("data-cod");
    if (!cod) return;
    if (btn.classList.contains("btn-edit-cd")) abrirEditar(cod);
    if (btn.classList.contains("btn-del-cd")) eliminar(cod);
  }

  function init() {
    if (window.__codigosDetalleInited) return;
    var req = [
      "filtro-cod",
      "btn-nuevo-cod",
      "tbl-codigos",
      "lbl-total-cod",
      "cd-modal",
      "form-cd-modal",
      "btn-close-cd-modal",
      "btn-cancel-cd-modal",
    ];
    var missing = req.filter(function (id) {
      return !byId(id);
    });
    if (missing.length) {
      toast("Faltan elementos: " + missing.join(", "), "error");
      return;
    }
    window.__codigosDetalleInited = true;

    byId("btn-nuevo-cod").addEventListener("click", abrirNuevo);
    byId("filtro-cod").addEventListener("input", renderTabla);
    byId("form-cd-modal").addEventListener("submit", guardar);
    byId("btn-close-cd-modal").addEventListener("click", function () {
      setModal(false);
      limpiarModal();
    });
    byId("btn-cancel-cd-modal").addEventListener("click", function () {
      setModal(false);
      limpiarModal();
    });
    byId("cd-modal").addEventListener("click", function (ev) {
      if (ev.target === byId("cd-modal")) {
        setModal(false);
        limpiarModal();
      }
    });
    byId("tbl-codigos").addEventListener("click", onTblClick);

    recargar();
  }

  window.codigosDetallePageReady = init;
})();
