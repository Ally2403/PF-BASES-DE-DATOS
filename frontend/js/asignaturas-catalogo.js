(function () {
  function $(id) {
    return document.getElementById(id);
  }

  function esc(t) {
    var d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  var asigCache = [];
  var programasCache = [];

  function setModalOpen(id, open) {
    var modal = $(id);
    if (!modal) return;
    modal.classList.toggle("open", !!open);
    modal.setAttribute("aria-hidden", open ? "false" : "true");
  }

  function getFiltrados() {
    var q = $("filtro-asig").value.trim().toLowerCase();
    if (!q) return [...asigCache];
    return asigCache.filter(function (a) {
      return String(a.nombre || "").toLowerCase().includes(q);
    });
  }

  function renderTabla() {
    var rows = getFiltrados();
    var tb = $("tbl-asig");
    tb.innerHTML = "";
    rows.forEach(function (r) {
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        esc(r.nombre) +
        "</td><td>" +
        esc(r.cant_creditos) +
        "</td><td>" +
        '<div class="btn-row">' +
        '<button type="button" class="btn btn-secondary btn-edit-asig" data-id="' +
        esc(r.id_asignatura) +
        '">Editar</button>' +
        '<button type="button" class="btn btn-danger btn-del-asig" data-id="' +
        esc(r.id_asignatura) +
        '">Eliminar</button>' +
        "</div>" +
        "</td>";
      tb.appendChild(tr);
    });
    $("lbl-total-asig").textContent =
      "Mostrando " + rows.length + " de " + asigCache.length + " registros.";
  }

  async function recargarCatalogo() {
    try {
      asigCache = await api.getCatalogoAsignaturas();
      renderTabla();
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  async function recargarProgramasParaPlan() {
    programasCache = await api.getProgramas();
    var sel = $("pea-prog");
    sel.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija programa —";
    sel.appendChild(ph);
    programasCache.forEach(function (p) {
      var o = document.createElement("option");
      o.value = p.id_programa;
      o.textContent = p.nombre_programa;
      sel.appendChild(o);
    });
  }

  function recargarAsignaturasSelectPlan() {
    var sel = $("pea-asig");
    sel.innerHTML = "";
    asigCache.forEach(function (a) {
      var o = document.createElement("option");
      o.value = a.id_asignatura;
      o.textContent = a.nombre + " (" + a.cant_creditos + " cr.)";
      sel.appendChild(o);
    });
  }

  function limpiarModalAsig() {
    $("asig-id").value = "";
    $("asig-nombre").value = "";
    $("asig-cred").value = "";
  }

  function abrirModalNuevo() {
    limpiarModalAsig();
    $("asig-modal-title").textContent = "Nueva asignatura";
    setModalOpen("asig-modal", true);
  }

  async function abrirModalEditar(id) {
    try {
      var list = await api.getCatalogoAsignaturas();
      var row = list.find(function (x) { return Number(x.id_asignatura) === Number(id); });
      if (!row) throw new Error("Asignatura no encontrada.");
      $("asig-id").value = String(row.id_asignatura);
      $("asig-nombre").value = row.nombre || "";
      $("asig-cred").value = String(row.cant_creditos ?? "");
      $("asig-modal-title").textContent = "Editar asignatura";
      setModalOpen("asig-modal", true);
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  async function guardarAsignatura(ev) {
    ev.preventDefault();
    var id = Number($("asig-id").value);
    var nombre = $("asig-nombre").value.trim();
    var cred = Number($("asig-cred").value);
    if (!nombre) {
      auth.showToast("Nombre obligatorio", "error");
      return;
    }
    if (nombre.length < 3) {
      auth.showToast("Nombre debe tener al menos 3 caracteres", "error");
      return;
    }
    if (!Number.isInteger(cred) || cred < 1 || cred > 20) {
      auth.showToast("Créditos debe ser un número entero entre 1 y 20", "error");
      return;
    }
    try {
      if (!id) {
        await api.postAsignaturaCatalog({ nombre: nombre, cant_creditos: cred });
        auth.showToast("Asignatura creada");
      } else {
        await api.putAsignaturaCatalog(id, { nombre: nombre, cant_creditos: cred });
        auth.showToast("Asignatura actualizada");
      }
      setModalOpen("asig-modal", false);
      limpiarModalAsig();
      await recargarCatalogo();
      recargarAsignaturasSelectPlan();
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  async function eliminarAsignatura(id) {
    if (!await auth.showConfirm("¿Desea eliminar esta asignatura del catálogo? Esta acción no se puede deshacer.")) return;
    if (!await auth.showConfirmCedula(
      "Está a punto de eliminar esta asignatura del catálogo institucional.",
      "Si la asignatura está vinculada a algún plan de estudios activo, la eliminación será bloqueada. De lo contrario, se eliminará permanentemente y no podrá usarse en futuros planes de cobro por créditos."
    )) return;
    try {
      await api.deleteAsignaturaCatalog(id);
      auth.showToast("Asignatura eliminada");
      await recargarCatalogo();
      recargarAsignaturasSelectPlan();
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  async function peaVincular() {
    var pid = Number($("pea-prog").value);
    var sem = Number($("pea-sem").value);
    var aid = Number($("pea-asig").value);
    if (!pid || !sem || !aid) {
      auth.showToast("Seleccione programa, semestre y asignatura.", "error");
      return;
    }
    try {
      await api.postPlanEstudioAsignatura(pid, sem, aid);
      auth.showToast("Asignatura vinculada al plan");
      $("pea-sem").value = "";
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  async function peaQuitar() {
    var pid = Number($("pea-prog").value);
    var sem = Number($("pea-sem").value);
    var aid = Number($("pea-asig").value);
    if (!pid || !sem || !aid) {
      auth.showToast("Seleccione programa, semestre y asignatura.", "error");
      return;
    }
    if (!await auth.showConfirm("¿Desea quitar esta asignatura del plan de estudios?")) return;
    if (!await auth.showConfirmCedula(
      "Está a punto de quitar una asignatura del plan de estudios.",
      "Al retirarla del plan, no se contabilizará en el cálculo de créditos para futuros cobros de matrícula por créditos. Los volantes ya generados no se modifican."
    )) return;
    try {
      await api.deletePlanEstudioAsignatura(pid, sem, aid);
      auth.showToast("Asignatura quitada del plan");
      $("pea-sem").value = "";
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    $("btn-nuevo-asig").addEventListener("click", abrirModalNuevo);
    $("form-asig-modal").addEventListener("submit", guardarAsignatura);
    $("btn-close-asig-modal").addEventListener("click", function () {
      setModalOpen("asig-modal", false);
      limpiarModalAsig();
    });
    $("btn-cancel-asig-modal").addEventListener("click", function () {
      setModalOpen("asig-modal", false);
      limpiarModalAsig();
    });
    $("asig-modal").addEventListener("click", function (ev) {
      if (ev.target === $("asig-modal")) {
        setModalOpen("asig-modal", false);
        limpiarModalAsig();
      }
    });
    $("filtro-asig").addEventListener("input", renderTabla);
    $("tbl-asig").addEventListener("click", function (ev) {
      var btn = ev.target.closest("button");
      if (!btn) return;
      var id = Number(btn.dataset.id);
      if (!id) return;
      if (btn.classList.contains("btn-edit-asig")) abrirModalEditar(id);
      if (btn.classList.contains("btn-del-asig")) eliminarAsignatura(id);
    });

    $("btn-pea-add").addEventListener("click", peaVincular);
    $("btn-pea-del").addEventListener("click", peaQuitar);

    Promise.resolve()
      .then(recargarCatalogo)
      .then(function () {
        recargarAsignaturasSelectPlan();
        return recargarProgramasParaPlan();
      })
      .catch(function (e) {
        auth.showToast(e.message, "error");
      });
  });
})();
