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
      var bloqueado = !!r.tiene_movimientos;
      var btnEliminar = bloqueado
        ? `<span
             style="display:inline-flex;align-items:center;gap:.35rem;font-size:.8rem;
                    color:var(--text-muted);background:var(--surface-alt,#f3f4f6);
                    border:1px solid var(--border,#d1d5db);border-radius:4px;
                    padding:.2rem .55rem;cursor:default;white-space:nowrap"
             title="No se puede eliminar: este c\u00f3digo tiene movimientos financieros registrados. Los c\u00f3digos con historial no pueden eliminarse.">
             \uD83D\uDD12 Sin eliminar
           </span>`
        : `<button type="button" class="btn btn-danger btn-del-cd" data-cod="${cod}">Eliminar</button>`;
      tr.innerHTML = `
        <td><code>${cod}</code></td>
        <td>${esc(r.grupo)}</td>
        <td>${esc(r.descripcion)}</td>
        <td>${r.valor_defecto ? COP.format(r.valor_defecto) : '<span style="color:var(--text-muted)">N/A</span>'}</td>
        <td>
          <div class="btn-row">
            <button type="button" class="btn btn-secondary btn-edit-cd" data-cod="${cod}">Editar</button>
            ${btnEliminar}
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

  function actualizarEstadoValor() {
    var grupo = byId("cd-grupo") ? byId("cd-grupo").value : "COBRO";
    var campoValor = byId("cd-valor");
    var helpValor = campoValor && campoValor.nextElementSibling;
    var infoPago = byId("cd-info-pago");
    if (!campoValor) return;
    if (grupo === "PAGO") {
      campoValor.value = "";
      campoValor.disabled = true;
      campoValor.placeholder = "No aplica para pagos";
      if (helpValor && helpValor.tagName === "SMALL") {
        helpValor.textContent = "Los c\u00f3digos de tipo PAGO no pueden tener un valor por defecto.";
      }
      if (infoPago) infoPago.style.display = "block";
    } else {
      campoValor.disabled = false;
      campoValor.placeholder = "Ej: 85000";
      if (helpValor && helpValor.tagName === "SMALL") {
        helpValor.textContent = "Opcional. Si se ingresa, debe ser mayor a 0. En pesos colombianos (COP).";
      }
      if (infoPago) infoPago.style.display = "none";
    }
  }

  function limpiarModal() {
    byId("cd-form-mode").value = "new";
    byId("cd-codigo").value = "";
    byId("cd-codigo").readOnly = false;
    byId("cd-grupo").value = "COBRO";
    byId("cd-desc").value = "";
    if (byId("cd-valor")) byId("cd-valor").value = "";
    actualizarEstadoValor();
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
    if (byId("cd-valor")) byId("cd-valor").value = r.grupo === "PAGO" ? "" : (r.valor_defecto || "");
    actualizarEstadoValor();
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
    if (!/^[A-Z0-9_]{2,4}$/.test(codIn)) {
      toast("Código: 2–4 caracteres, solo letras, números o _", "error");
      return;
    }
    if (desc.length < 3) {
      toast("Descripción debe tener al menos 3 caracteres.", "error");
      return;
    }
    if (grupo === "PAGO" && val !== null) {
      toast("Los c\u00f3digos de tipo PAGO no pueden tener valor por defecto.", "error");
      if (byId("cd-valor")) byId("cd-valor").value = "";
      return;
    }
    if (grupo === "COBRO" && (val === null || val <= 0)) {
      toast("Los c\u00f3digos de tipo COBRO requieren un valor por defecto mayor a 0.", "error");
      return;
    }
    if (val !== null && val <= 0) {
      toast("El valor por defecto debe ser mayor a 0.", "error");
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
    if (!await auth.showConfirm("¿Desea eliminar el código \u201c" + key + "\u201d? Esta acción no se puede deshacer.")) return;
    if (!await auth.showConfirmCedula(
      "Está a punto de eliminar el concepto financiero \u201c" + key + "\u201d del catálogo.",
      "Este código clasifica movimientos en la cuenta corriente de los estudiantes. Solo puede eliminarse si no tiene movimientos registrados. Si existe algún historial, la eliminación será bloqueada por la base de datos."
    )) return;
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
    if (byId("cd-grupo")) byId("cd-grupo").addEventListener("change", actualizarEstadoValor);
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
