(function () {
  function $(id) {
    return document.getElementById(id);
  }

  function esc(t) {
    var d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  var programasCache = [];

  function programaSeleccionadoId() {
    var sel = $("sel-prog-plan");
    if (!sel || !sel.value) return null;
    return Number(sel.value);
  }

  function setModalOpen(id, open) {
    var modal = $(id);
    if (!modal) return;
    modal.classList.toggle("open", !!open);
    modal.setAttribute("aria-hidden", open ? "false" : "true");
  }

  function getFiltrados() {
    var q = $("filtro-prog").value.trim().toLowerCase();
    if (!q) return [...programasCache];
    return programasCache.filter(function (p) {
      return (
        String(p.nombre_programa || "").toLowerCase().includes(q) ||
        String(p.codigo_programa || "").toLowerCase().includes(q)
      );
    });
  }

  function renderTabla() {
    var list = getFiltrados();
    var tb = $("tbl-programas");
    tb.innerHTML = "";
    list.forEach(function (p) {
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td><code>" +
        esc(p.codigo_programa) +
        "</code></td><td>" +
        esc(p.nombre_programa) +
        "</td><td>" +
        '<div class="btn-row">' +
        '<button type="button" class="btn btn-secondary btn-edit-prog" data-id="' +
        esc(p.id_programa) +
        '">Editar</button>' +
        '<button type="button" class="btn btn-danger btn-del-prog" data-id="' +
        esc(p.id_programa) +
        '">Eliminar</button>' +
        "</div>" +
        "</td>";
      tb.appendChild(tr);
    });
    $("lbl-total-prog").textContent =
      "Mostrando " + list.length + " de " + programasCache.length + " registros.";
  }

  async function llenarSelectorProgramas() {
    var list = await api.getProgramas();
    programasCache = list;
    var sel = $("sel-prog-plan");
    var prev = sel.value;
    sel.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija programa —";
    sel.appendChild(ph);
    list.forEach(function (p) {
      var o = document.createElement("option");
      o.value = p.id_programa;
      o.textContent = p.id_programa + " — " + p.nombre_programa;
      sel.appendChild(o);
    });
    if (prev && list.some(function (x) { return String(x.id_programa) === String(prev); })) {
      sel.value = prev;
    } else if (list.length) {
      sel.selectedIndex = 1;
    }
  }

  function limpiarFormProgramaModal() {
    $("prog-id").value = "";
    $("prog-nombre").value = "";
    $("prog-codigo").value = "";
  }

  function abrirModalNuevo() {
    limpiarFormProgramaModal();
    $("prog-modal-title").textContent = "Nuevo programa";
    setModalOpen("prog-modal", true);
  }

  async function abrirModalEditar(id) {
    try {
      var list = await api.getProgramas({ id_programa: id });
      if (!list.length) throw new Error("Programa no encontrado");
      $("prog-id").value = String(list[0].id_programa);
      $("prog-nombre").value = list[0].nombre_programa || "";      $('prog-codigo').value = list[0].codigo_programa || "";      $("prog-modal-title").textContent = "Editar programa";
      setModalOpen("prog-modal", true);
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  var PROG_NOMBRE_RE = /^[A-Za-z\u00C0-\u024F\s]{3,200}$/;
  var PROG_CODIGO_RE = /^[A-Z0-9]{3}$/;

  async function guardarPrograma(ev) {
    ev.preventDefault();
    var id = Number($("prog-id").value);
    var nombre = $("prog-nombre").value.trim();
    var codigo = $("prog-codigo").value.trim().toUpperCase();
    if (!nombre) {
      auth.showToast("Nombre del programa obligatorio", "error");
      return;
    }
    if (!PROG_NOMBRE_RE.test(nombre)) {
      auth.showToast("Nombre: solo letras y espacios, mínimo 3 caracteres", "error");
      return;
    }
    if (!codigo) {
      auth.showToast("Código del programa obligatorio", "error");
      return;
    }
    if (!PROG_CODIGO_RE.test(codigo)) {
      auth.showToast("Código: exactamente 3 caracteres alfanuméricos (ej: SIS, ADM)", "error");
      return;
    }
    try {
      if (!id) {
        await api.postPrograma({ nombre_programa: nombre, codigo_programa: codigo });
        auth.showToast("Programa creado");
      } else {
        await api.putPrograma(id, { nombre_programa: nombre, codigo_programa: codigo });
        auth.showToast("Programa actualizado");
      }
      setModalOpen("prog-modal", false);
      limpiarFormProgramaModal();
      await llenarSelectorProgramas();
      renderTabla();
      await pintarPlanVista();
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  async function eliminarPrograma(id) {
    if (!await auth.showConfirm("¿Desea eliminar este programa? Esta acción no se puede deshacer.")) return;
    if (!await auth.showConfirmCedula(
      "Está a punto de eliminar un programa académico.",
      "Se eliminarán el plan de estudios y las reglas de cobro asociadas al programa. Los estudiantes inscritos y sus volantes ya generados impedirán la eliminación si existen dependencias activas."
    )) return;
    try {
      await api.deletePrograma(id);
      auth.showToast("Programa eliminado");
      await llenarSelectorProgramas();
      renderTabla();
      await pintarPlanVista();
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  async function pintarPlanVista() {
    var pid = programaSeleccionadoId();
    var wrap = $("plan-vista-cont");
    if (!pid) {
      wrap.innerHTML =
        "<p class=\"alert alert-info mb-0\">Seleccione un programa para ver su plan.</p>";
      return;
    }
    var filtroSem = $("filtro-sem-plan").value;
    var bloques = await api.getPlanPorPrograma(pid);
    var nom = $("sel-prog-plan").selectedOptions[0]
      ? $("sel-prog-plan").selectedOptions[0].textContent
      : "";

    var rows = [];
    var totalCreds = 0;
    bloques.forEach(function (b) {
      if (filtroSem && String(b.semestre) !== String(filtroSem)) return;
      b.asignaturas.forEach(function (a) {
        const c = Number(a.cant_creditos || 0);
        totalCreds += c;
        rows.push({
          semestre: b.semestre,
          id_asignatura: a.id_asignatura,
          nombre: a.nombre,
          cant_creditos: c,
        });
      });
    });
    rows.sort(function (x, y) {
      if (x.semestre !== y.semestre) return x.semestre - y.semestre;
      return Number(x.id_asignatura) - Number(y.id_asignatura);
    });

    var html =
      "<div style=\"display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; padding:0.75rem; background:rgba(99,102,241,0.05); border-radius:var(--radius-sm); border:1px solid rgba(99,102,241,0.1)\">" +
      "<p style=\"font-size:0.9rem; color:var(--text); margin:0\">Programa: <strong>" + esc(nom) + "</strong>" +
      (filtroSem ? " · Semestre: <strong>" + esc(filtroSem) + "</strong>" : "") +
      "</p>" +
      "<div style=\"text-align:right\"><span style=\"display:block; font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em\">Carga Académica Total</span>" +
      "<span style=\"font-size:1.25rem; font-weight:800; color:var(--accent-light)\">" + totalCreds + " <small style='font-size:0.7rem; font-weight:400'>Créditos</small></span></div>" +
      "</div>";

    html +=
      "<div class=\"table-wrap\"><table><thead><tr><th>SEMESTRE</th><th>NOMBRE</th><th>CREDITOS</th></tr></thead><tbody>";
    if (!rows.length) {
      html +=
        "<tr><td colspan=\"4\">No hay filas para este filtro (o el plan no tiene asignaturas).</td></tr>";
    } else {
      rows.forEach(function (r) {
        html +=
          "<tr><td>" +
          esc(r.semestre) +
          "</td><td>" +
          esc(r.nombre) +
          "</td><td>" +
          esc(r.cant_creditos) +
          "</td></tr>";
      });
    }
    html += "</tbody></table></div>";

    wrap.innerHTML = html;
  }

  document.addEventListener("DOMContentLoaded", async function () {
    $("btn-nuevo-prog").addEventListener("click", abrirModalNuevo);
    $("form-prog-modal").addEventListener("submit", guardarPrograma);
    $("btn-close-prog-modal").addEventListener("click", function () {
      setModalOpen("prog-modal", false);
      limpiarFormProgramaModal();
    });
    $("btn-cancel-prog-modal").addEventListener("click", function () {
      setModalOpen("prog-modal", false);
      limpiarFormProgramaModal();
    });
    $("prog-modal").addEventListener("click", function (ev) {
      if (ev.target === $("prog-modal")) {
        setModalOpen("prog-modal", false);
        limpiarFormProgramaModal();
      }
    });
    $("filtro-prog").addEventListener("input", renderTabla);
    $("tbl-programas").addEventListener("click", function (ev) {
      var btn = ev.target.closest("button");
      if (!btn) return;
      var id = Number(btn.dataset.id);
      if (!id) return;
      if (btn.classList.contains("btn-edit-prog")) abrirModalEditar(id);
      if (btn.classList.contains("btn-del-prog")) eliminarPrograma(id);
    });

    $("sel-prog-plan").addEventListener("change", function () {
      void pintarPlanVista();
    });
    $("filtro-sem-plan").addEventListener("change", function () {
      void pintarPlanVista();
    });

    $("btn-add-sem").addEventListener("click", function () {
      var pid = programaSeleccionadoId();
      if (!pid) {
        auth.showToast("Seleccione un programa.", "error");
        return;
      }
      $("sem-num").value = "";
      setModalOpen("sem-modal", true);
    });
    $("form-sem-modal").addEventListener("submit", async function (ev) {
      ev.preventDefault();
      var pid = programaSeleccionadoId();
      if (!pid) {
        auth.showToast("Seleccione un programa.", "error");
        return;
      }
      try {
        await api.postPlanEstudioSemestre(pid, Number($("sem-num").value));
        auth.showToast("Semestre agregado al plan");
        $("sem-num").value = "";
        setModalOpen("sem-modal", false);
        await pintarPlanVista();
      } catch (e) {
        auth.showToast(e.message, "error");
      }
    });
    $("btn-close-sem-modal").addEventListener("click", function () {
      setModalOpen("sem-modal", false);
    });
    $("btn-cancel-sem-modal").addEventListener("click", function () {
      setModalOpen("sem-modal", false);
    });
    $("sem-modal").addEventListener("click", function (ev) {
      if (ev.target === $("sem-modal")) setModalOpen("sem-modal", false);
    });
    // Quitar semestre: use el modal o la vista de semestres en Asignaturas (catálogo) si se requiere.

    await llenarSelectorProgramas();
    renderTabla();
    await pintarPlanVista();
  });
})();
