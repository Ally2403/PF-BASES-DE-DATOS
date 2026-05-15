/**
 * Reglas de cobro: tabla + búsqueda + modal crear/editar.
 */
(function () {
  var COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  function byId(id) {
    return document.getElementById(id);
  }

  function esc(t) {
    var d = document.createElement("div");
    d.textContent = t === null || t === undefined ? "" : String(t);
    return d.innerHTML;
  }

  var programasCache = [];
  var periodosCache = [];
  var reglasVista = [];

  function setModal(open) {
    var m = byId("rc-modal");
    if (!m) return;
    if (open) m.classList.add("open");
    else m.classList.remove("open");
    m.setAttribute("aria-hidden", open ? "false" : "true");
  }

  function toast(msg, kind) {
    if (window.auth && typeof auth.showToast === "function") {
      auth.showToast(msg, kind || "error");
    } else {
      window.alert(msg);
    }
  }

  function nombrePrograma(id) {
    var p = programasCache.find(function (x) {
      return Number(x.id_programa) === Number(id);
    });
    return p ? p.nombre_programa : "";
  }

  function nombrePeriodo(id) {
    var p = periodosCache.find(function (x) {
      return Number(x.id_periodo) === Number(id);
    });
    return p ? p.nombre_periodo : "";
  }

  function enriquecerLista(list) {
    return list.map(function (r) {
      return {
        modalidad: r.modalidad,
        id_programa: r.id_programa,
        id_periodo: r.id_periodo,
        valorglobal: r.valorglobal,
        valorcredito: r.valorcredito,
        _nom_prog: nombrePrograma(r.id_programa),
        _nom_per: nombrePeriodo(r.id_periodo),
      };
    });
  }

  function filtrarVista() {
    var inp = byId("filtro-regla");
    var q = inp && inp.value ? inp.value.trim().toLowerCase() : "";
    if (!q) return reglasVista.slice();
    return reglasVista.filter(function (r) {
      var blob =
        String(r.modalidad || "").toLowerCase() +
        " " +
        String(r._nom_prog || "").toLowerCase() +
        " " +
        String(r._nom_per || "").toLowerCase();
      return blob.indexOf(q) !== -1;
    });
  }

  function renderTabla() {
    var tb = byId("tbl-reglas");
    var lbl = byId("lbl-total-regla");
    if (!tb) return;
    var rows = filtrarVista();
    tb.innerHTML = "";
    rows.forEach(function (r) {
      var tr = document.createElement("tr");
      var vg =
        r.valorglobal != null && r.valorglobal !== ""
          ? COP.format(Number(r.valorglobal))
          : "—";
      var vc =
        r.valorcredito != null && r.valorcredito !== ""
          ? COP.format(Number(r.valorcredito))
          : "—";
      tr.innerHTML =
        "<td>" +
        esc(r.modalidad) +
        "</td><td>" +
        esc(r._nom_prog || r.id_programa) +
        "</td><td>" +
        esc(r._nom_per || r.id_periodo) +
        "</td>" +
        "<td class=\"numeric\">" +
        vg +
        "</td>" +
        "<td class=\"numeric\">" +
        vc +
        "</td>" +
        "<td>" +
        '<div class="btn-row">' +
        '<button type="button" class="btn btn-secondary btn-edit-rc" data-prog="' +
        esc(r.id_programa) +
        '" data-per="' +
        esc(r.id_periodo) +
        '" data-mod="' +
        esc(r.modalidad) +
        '">Editar</button>' +
        '<button type="button" class="btn btn-danger btn-del-rc" data-prog="' +
        esc(r.id_programa) +
        '" data-per="' +
        esc(r.id_periodo) +
        '" data-mod="' +
        esc(r.modalidad) +
        '">Eliminar</button>' +
        "</div>" +
        "</td>";
      tb.appendChild(tr);
    });
    if (lbl) {
      lbl.textContent =
        "Mostrando " + rows.length + " de " + reglasVista.length + " registros.";
    }
  }

  function llenarSelectProgramas(sel, keepVal) {
    if (!sel) return;
    var v = keepVal != null ? String(keepVal) : sel.value;
    sel.innerHTML = "";
    programasCache.forEach(function (p) {
      var o = document.createElement("option");
      o.value = p.id_programa;
      o.textContent = p.nombre_programa;
      sel.appendChild(o);
    });
    if (v && programasCache.some(function (x) { return String(x.id_programa) === v; })) {
      sel.value = v;
    }
  }

  function llenarSelectPeriodos(sel, keepVal) {
    if (!sel) return;
    var v = keepVal != null ? String(keepVal) : sel.value;
    sel.innerHTML = "";
    periodosCache.forEach(function (p) {
      var o = document.createElement("option");
      o.value = p.id_periodo;
      o.textContent = p.nombre_periodo;
      sel.appendChild(o);
    });
    if (v && periodosCache.some(function (x) { return String(x.id_periodo) === v; })) {
      sel.value = v;
    }
  }

  function toggleCamposValor() {
    var mod = byId("rc-modalidad") ? byId("rc-modalidad").value : "GLOBAL";
    var wG = byId("wrap-rc-global");
    var wC = byId("wrap-rc-cred");
    if (mod === "GLOBAL") {
      if (wG) wG.style.display = "";
      if (wC) wC.style.display = "none";
    } else {
      if (wG) wG.style.display = "none";
      if (wC) wC.style.display = "";
    }
  }

  function setSelectsBloqueados(bloqueado) {
    var s = ["rc-programa", "rc-periodo", "rc-modalidad"];
    for (var i = 0; i < s.length; i++) {
      var el = byId(s[i]);
      if (el) el.disabled = !!bloqueado;
    }
  }

  function limpiarModal() {
    byId("rc-form-mode").value = "new";
    byId("rc-val-global").value = "";
    byId("rc-val-cred").value = "";
    if (byId("rc-modalidad")) byId("rc-modalidad").value = "GLOBAL";
    setSelectsBloqueados(false);
    toggleCamposValor();
  }

  function abrirModalNuevo() {
    limpiarModal();
    var title = byId("rc-modal-title");
    if (title) title.textContent = "Nueva regla";
    llenarSelectProgramas(byId("rc-programa"));
    llenarSelectPeriodos(byId("rc-periodo"));
    setModal(true);
  }

  function abrirModalEditar(prog, per, mod) {
    var r = reglasVista.find(function (x) {
      return (
        Number(x.id_programa) === Number(prog) &&
        Number(x.id_periodo) === Number(per) &&
        String(x.modalidad) === String(mod)
      );
    });
    if (!r) {
      toast("Regla no encontrada.", "error");
      return;
    }
    byId("rc-form-mode").value = "edit";
    llenarSelectProgramas(byId("rc-programa"), r.id_programa);
    llenarSelectPeriodos(byId("rc-periodo"), r.id_periodo);
    byId("rc-modalidad").value = String(r.modalidad);
    byId("rc-val-global").value =
      r.valorglobal != null ? String(r.valorglobal) : "";
    byId("rc-val-cred").value =
      r.valorcredito != null ? String(r.valorcredito) : "";
    var title = byId("rc-modal-title");
    if (title) title.textContent = "Editar regla";
    setSelectsBloqueados(true);
    toggleCamposValor();
    setModal(true);
  }

  async function guardar(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var modo = byId("rc-form-mode").value;
    var pid = Number(byId("rc-programa").value);
    var per = Number(byId("rc-periodo").value);
    var mod = String(byId("rc-modalidad").value || "").toUpperCase();
    var vg = byId("rc-val-global").value.trim();
    var vc = byId("rc-val-cred").value.trim();

    try {
      if (!window.api) throw new Error("api no disponible");
      if (!pid) {
        toast("Seleccione un programa académico.", "error");
        return;
      }
      if (!per) {
        toast("Seleccione un período.", "error");
        return;
      }
      if (mod === "GLOBAL" && (!vg || Number(vg) <= 0)) {
        toast("Ingrese un valor global mayor a 0.", "error");
        return;
      }
      if (mod === "CREDITO" && (!vc || Number(vc) <= 0)) {
        toast("Ingrese un valor por crédito mayor a 0.", "error");
        return;
      }
      if (modo === "new") {
        var body = {
          id_programa: pid,
          id_periodo: per,
          modalidad: mod,
        };
        if (mod === "GLOBAL") {
          body.valorglobal = Number(vg);
        } else {
          body.valorcredito = Number(vc);
        }
        await api.postReglaCobro(body);
        toast("Regla creada", "success");
      } else {
        var bodyPut = {};
        if (mod === "GLOBAL") bodyPut.valorglobal = Number(vg);
        else bodyPut.valorcredito = Number(vc);
        await api.putReglaCobro(pid, per, mod, bodyPut);
        toast("Regla actualizada", "success");
      }
      setModal(false);
      limpiarModal();
      await recargar();
    } catch (e) {
      toast(e.message || "Error al guardar", "error");
    }
  }

  async function eliminar(prog, per, mod) {
    if (!await auth.showConfirm("¿Desea eliminar esta regla de cobro? Esta acción no se puede deshacer.")) return;
    if (!await auth.showConfirmCedula(
      "Está a punto de eliminar una regla de cobro.",
      "Esta regla define cómo se calculan los montos de matrícula para el programa y período seleccionados. Sin ella, no se podrán generar nuevos volantes de cobro. Los volantes ya emitidos no se verán afectados, pero futuros cobros quedarán bloqueados."
    )) return;
    try {
      await api.deleteReglaCobro(prog, per, mod);
      toast("Regla eliminada", "success");
      await recargar();
    } catch (e) {
      toast(e.message || "No se pudo eliminar", "error");
    }
  }

  async function recargar() {
    try {
      if (typeof api.getReglasCobro !== "function") {
        toast("getReglasCobro no está en api.js", "error");
        return;
      }
      programasCache = await api.getProgramas();
      periodosCache = await api.getPeriodos();
      var raw = await api.getReglasCobro();
      if (!Array.isArray(raw)) raw = [];
      reglasVista = enriquecerLista(raw);
      renderTabla();
    } catch (e) {
      toast(e.message || "Error al cargar reglas", "error");
    }
  }

  function init() {
    if (window.__reglasCobroInited) return;
    var req = [
      "filtro-regla",
      "btn-nueva-regla",
      "tbl-reglas",
      "lbl-total-regla",
      "rc-modal",
      "form-rc-modal",
      "btn-close-rc-modal",
      "btn-cancel-rc-modal",
    ];
    var missing = req.filter(function (id) { return !byId(id); });
    if (missing.length) {
      toast("Faltan elementos: " + missing.join(", "), "error");
      return;
    }
    window.__reglasCobroInited = true;

    byId("btn-nueva-regla").addEventListener("click", abrirModalNuevo);
    byId("filtro-regla").addEventListener("input", renderTabla);
    byId("form-rc-modal").addEventListener("submit", guardar);
    byId("rc-modalidad").addEventListener("change", toggleCamposValor);
    byId("btn-close-rc-modal").addEventListener("click", function () {
      setModal(false);
      limpiarModal();
    });
    byId("btn-cancel-rc-modal").addEventListener("click", function () {
      setModal(false);
      limpiarModal();
    });
    byId("rc-modal").addEventListener("click", function (ev) {
      if (ev.target === byId("rc-modal")) {
        setModal(false);
        limpiarModal();
      }
    });
    byId("tbl-reglas").addEventListener("click", function (ev) {
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
      var prog = btn.getAttribute("data-prog");
      var per = btn.getAttribute("data-per");
      var m = btn.getAttribute("data-mod");
      if (btn.classList.contains("btn-edit-rc")) {
        abrirModalEditar(prog, per, m);
      }
      if (btn.classList.contains("btn-del-rc")) {
        eliminar(Number(prog), Number(per), m);
      }
    });

    recargar();
  }

  window.reglasCobroPageReady = init;
})();
