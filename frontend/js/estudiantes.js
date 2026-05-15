(function () {
  function qs(id) {
    return document.getElementById(id);
  }

  let programasCache = [];
  let estudiantesCache = [];

  async function cargarProgramas() {
    const raw = await api.getProgramas();
    programasCache = Array.isArray(raw) ? raw : [];
    const selEdit = qs("edit-id_programa");
    selEdit.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija programa —";
    selEdit.appendChild(ph);
    programasCache.forEach(function (p) {
      const o = document.createElement("option");
      o.value = p.id_programa;
      o.textContent = p.nombre_programa;
      selEdit.appendChild(o);
    });
  }

  function escapeHtml(t) {
    const d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  function setModalOpen(open) {
    const modal = qs("edit-est-modal");
    if (!modal) return;
    modal.classList.toggle("open", !!open);
    modal.setAttribute("aria-hidden", open ? "false" : "true");
  }

  function limpiarFormularioEdit() {
    qs("form-est-edit").reset();
    qs("edit-id_estudiante").value = "";
    if (qs("edit-id_programa").options.length) qs("edit-id_programa").selectedIndex = 0;
  }

  async function recargar() {
    try {
      estudiantesCache = await api.getEstudiantes();
      renderTabla();
    } catch (err) {
      auth.showToast(err.message || "Error al cargar", "error");
    }
  }

  function getFiltrados() {
    const q = qs("filtro-est").value.trim().toLowerCase();
    if (!q) return [...estudiantesCache];
    return estudiantesCache.filter(function (e) {
      const full = (e.nombre + " " + e.apellido).toLowerCase();
      return (
        String(e.nombre || "").toLowerCase().includes(q) ||
        String(e.apellido || "").toLowerCase().includes(q) ||
        full.includes(q) ||
        String(e.carnet || "").toLowerCase().includes(q) ||
        String(e.correo || "").toLowerCase().includes(q)
      );
    });
  }

  function renderTabla() {
    const list = getFiltrados();
    const tb = qs("tbl-body");
    tb.innerHTML = "";
    list.forEach(function (e) {
      const tr = document.createElement("tr");
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
        escapeHtml(e.telefono) +
        "</td><td>" +
        escapeHtml(e.nombre_programa) +
        "</td><td>" +
        '<div class="btn-row">' +
        '<button type="button" class="btn btn-secondary btn-edit-est" data-id="' +
        escapeHtml(e.id_estudiante) +
        '">Editar</button>' +
        '<button type="button" class="btn btn-danger btn-del-est" data-id="' +
        escapeHtml(e.id_estudiante) +
        '">Eliminar</button>' +
        "</div>" +
        "</td>";
      tb.appendChild(tr);
    });
    qs("lbl-total-est").textContent =
      "Mostrando " + list.length + " de " + estudiantesCache.length + " registros.";
  }

  function llenarEditForm(e) {
    qs("edit-id_estudiante").value = String(e.id_estudiante);
    qs("edit-carnet").value = e.carnet || "";
    qs("edit-nombre").value = e.nombre || "";
    qs("edit-apellido").value = e.apellido || "";
    qs("edit-telefono").value = e.telefono || "";
    qs("edit-correo").value = e.correo || "";
    qs("edit-id_programa").value = String(e.id_programa);
  }

  function abrirModalNuevo() {
    limpiarFormularioEdit();
    qs("edit-est-title").textContent = "Nuevo estudiante";
    // Ocultar solo el carnet (se genera en el backend), dejar visible el programa
    var carnetField = qs("carnet-row");
    if (carnetField) carnetField.style.display = "none";
    var progSel = qs("edit-id_programa");
    if (progSel) { progSel.disabled = false; progSel.required = true; }
    setModalOpen(true);
  }

  async function abrirModalEditar(id) {
    try {
      const e = await api.getEstudiante(Number(id));
      llenarEditForm(e);
      qs("edit-est-title").textContent = "Editar estudiante";
      // Mostrar el carnet (readonly); permitir cambio de programa (regenera carnet)
      var carnetField = qs("carnet-row");
      if (carnetField) carnetField.style.display = "";
      var progSel = qs("edit-id_programa");
      if (progSel) { progSel.disabled = false; progSel.required = true; }
      setModalOpen(true);
    } catch (e) {
      auth.showToast(e.message, "error");
    }
  }

  // Validaciones del formulario de estudiantes
  const SOLO_LETRAS = /^[A-Za-z\u00C0-\u024F\s]+$/;
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const TELEFONO_RE = /^3[0-9]{9}$/

  function validarFormEstudiante(body, esNuevo) {
    const errs = [];
    if (!body.nombre) {
      errs.push("Nombre es obligatorio");
    } else if (body.nombre.length < 2) {
      errs.push("Nombre debe tener al menos 2 caracteres");
    } else if (!SOLO_LETRAS.test(body.nombre)) {
      errs.push("Nombre solo puede contener letras y espacios");
    }
    if (!body.apellido) {
      errs.push("Apellido es obligatorio");
    } else if (body.apellido.length < 2) {
      errs.push("Apellido debe tener al menos 2 caracteres");
    } else if (!SOLO_LETRAS.test(body.apellido)) {
      errs.push("Apellido solo puede contener letras y espacios");
    }
    if (!body.correo) {
      errs.push("Correo es obligatorio");
    } else if (!EMAIL_RE.test(body.correo)) {
      errs.push("Correo no tiene un formato válido");
    }
    if (body.telefono && !TELEFONO_RE.test(body.telefono)) {
      errs.push("Teléfono debe tener 10 dígitos y empezar por 3 (ej: 3001234567)");
    }
    if (!body.id_programa) {
      errs.push("Debe seleccionar un programa académico");
    }
    return errs;
  }

  async function actualizarExistente(ev) {
    ev.preventDefault();
    const id = Number(qs("edit-id_estudiante").value);
    const body = {
      nombre: qs("edit-nombre").value.trim(),
      apellido: qs("edit-apellido").value.trim(),
      telefono: qs("edit-telefono").value.trim(),
      correo: qs("edit-correo").value.trim(),
      id_programa: Number(qs("edit-id_programa").value),
    };
    const errs = validarFormEstudiante(body, !id);
    if (errs.length) {
      auth.showToast(errs[0], "error");
      return;
    }
    try {
      if (!id) {
        await api.postEstudiante(body);
        auth.showToast("Estudiante creado correctamente");
      } else {
        await api.putEstudiante(id, body);
        auth.showToast("Estudiante actualizado");
      }
      setModalOpen(false);
      limpiarFormularioEdit();
      await recargar();
    } catch (e) {
      auth.showToast(e.message || "No se pudo actualizar", "error");
    }
  }

  async function eliminarPorId(id) {
    const numId = Number(id);
    if (!numId) return;
    const row = estudiantesCache.find(function (e) {
      return Number(e.id_estudiante) === numId;
    });
    if (!Number.isFinite(numId) || numId < 1) {
      auth.showToast("ID_ESTUDIANTE inválido.", "error");
      return;
    }
    var nomEst = row ? row.nombre + " " + row.apellido : "ID " + id;
    if (!await auth.showConfirm("¿Desea eliminar al estudiante " + nomEst + "? Esta acción no se puede deshacer.")) {
      return;
    }
    if (!await auth.showConfirmCedula(
      "Está a punto de eliminar al estudiante <strong>" + nomEst + "</strong> del sistema.",
      "Se eliminarán todos sus datos personales, su cuenta corriente y el historial de movimientos financieros asociados. Esta acción es irreversible."
    )) {
      return;
    }
    try {
      await api.deleteEstudiante(numId);
      auth.showToast("Estudiante eliminado");
      await recargar();
    } catch (e) {
      auth.showToast(e.message || "No se pudo eliminar", "error");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    cargarProgramas().then(recargar);
    qs("filtro-est").addEventListener("input", renderTabla);
    qs("btn-nuevo-est").addEventListener("click", abrirModalNuevo);
    qs("tbl-body").addEventListener("click", function (ev) {
      const btn = ev.target.closest("button");
      if (!btn) return;
      const id = Number(btn.dataset.id);
      if (!id) return;
      if (btn.classList.contains("btn-edit-est")) abrirModalEditar(id);
      if (btn.classList.contains("btn-del-est")) eliminarPorId(id);
    });
    qs("form-est-edit").addEventListener("submit", actualizarExistente);
    qs("btn-close-modal").addEventListener("click", function () {
      setModalOpen(false);
      limpiarFormularioEdit();
    });
    qs("btn-cancel-modal").addEventListener("click", function () {
      setModalOpen(false);
      limpiarFormularioEdit();
    });
    qs("edit-est-modal").addEventListener("click", function (ev) {
      if (ev.target === qs("edit-est-modal")) {
        setModalOpen(false);
        limpiarFormularioEdit();
      }
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && qs("edit-est-modal").classList.contains("open")) {
        setModalOpen(false);
        limpiarFormularioEdit();
      }
    });
    limpiarFormularioEdit();
  });
})();
