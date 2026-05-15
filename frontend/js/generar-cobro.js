(function () {
  const COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  function $(id) {
    return document.getElementById(id);
  }

  let volActual = null;
  let estudiantesLista = [];
  let periodosLista = [];

  function listaEstudiantesBase() {
    return Array.isArray(estudiantesLista) ? estudiantesLista : [];
  }

  function escapeHtml(t) {
    const d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  function escAttr(t) {
    return String(t).replace(/"/g, "&quot;");
  }

  function getFiltradosEstudiantes() {
    const inp = $("gc-filtro-est");
    const q = inp && inp.value ? inp.value.trim().toLowerCase() : "";
    const base = listaEstudiantesBase();
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

  function puedeMantenerSeleccion(list) {
    const id = Number($("gc-est").value);
    if (!id) return true;
    return list.some(function (e) {
      return Number(e.id_estudiante) === id;
    });
  }

  function renderTablaEstudiantes() {
    const tb = $("gc-tbl-est");
    const lbl = $("gc-lbl-est");
    if (!tb) return;

    const baseTot = listaEstudiantesBase().length;
    if (baseTot === 0) {
      tb.innerHTML =
        '<tr><td colspan="5" style="color:var(--text-muted)">No hay estudiantes cargados. Revise la consola (F12), la sesión o que <code>api.js</code> cargue bien.</td></tr>';
      if (lbl) {
        lbl.innerHTML =
          "Si acaba de abrir la página, recargue. Con mock activo deberían aparecer filas de ejemplo.";
      }
      return;
    }

    const list = getFiltradosEstudiantes();
    tb.innerHTML = "";
    if (!puedeMantenerSeleccion(list)) {
      $("gc-est").value = "";
    }
    const currentSel = Number($("gc-est").value);

    if (!list.length) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        '<td colspan="5" style="color:var(--text-muted)">Sin coincidencias. Ajuste el filtro.</td>';
      tb.appendChild(tr);
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
        tb.appendChild(tr);
      });
    }

    const n = list.length;
    const tot = baseTot;
    const sel = $("gc-est").value;
    let selText = "";
    if (sel) {
      const e = listaEstudiantesBase().find(function (x) {
        return String(x.id_estudiante) === String(sel);
      });
      if (e) {
        selText =
          " · Seleccionado: <strong>" +
          escapeHtml(e.carnet) +
          " — " +
          escapeHtml(e.nombre) +
          " " +
          escapeHtml(e.apellido) +
          "</strong>";
      }
    }
    if (lbl) {
      lbl.innerHTML =
        "Mostrando " + n + " de " + tot + " estudiante(s)." + selText + " Pulse una fila para elegir.";
    }
  }

  async function seleccionarEstudiantePorId(id) {
    $('gc-est').value = String(id);
    renderTablaEstudiantes();
    // Ocultar resumen anterior al cambiar de estudiante
    $('resumen-final').hidden = true;
    volActual = null;
    
    // Request 1: Early validation of existing volante just after clicking student
    const idPer = Number($("gc-per").value);
    if (idPer && id) {
      const exists = await volanteYaExiste(id, idPer);
      if (exists) {
        $("gc-msg").textContent = "Este estudiante ya tiene volante en el período seleccionado.";
        $("gc-msg").hidden = false;
        $("gc-msg").className = "alert alert-error";
        $("btn-gen-paso1").disabled = true;
        return;
      } else {
        $("gc-msg").hidden = true;
      }
    }
    
    refrescarMontosPrincipal();
  }

  function bindGenerarCobroUi() {
    const form = $("form-paso1");
    if (!form || form.getAttribute("data-gc-bound") === "1") return;
    form.setAttribute("data-gc-bound", "1");

    function onFiltro() {
      renderTablaEstudiantes();
    }
    const filtro = $("gc-filtro-est");
    if (filtro) {
      filtro.addEventListener("input", onFiltro);
      filtro.addEventListener("keyup", onFiltro);
      filtro.addEventListener("search", onFiltro);
    }

    const tbl = $("gc-tbl-est");
    if (tbl) {
      tbl.addEventListener("click", function (ev) {
        const tr = ev.target.closest("tr");
        if (!tr || !tr.dataset.idEstudiante) return;
        seleccionarEstudiantePorId(Number(tr.dataset.idEstudiante));
      });
    }

    $("gc-per").addEventListener("change", refrescarMontosPrincipal);
    $("gc-sem").addEventListener("change", refrescarMontosPrincipal);
    $("gc-mod").addEventListener("change", refrescarMontosPrincipal);
    form.addEventListener("submit", generarPrincipal);
  }

  async function cargarCatalogos() {
    const rawEst = await api.getEstudiantes({});
    estudiantesLista =
      typeof api.normalizarListaEstudiantes === "function"
        ? api.normalizarListaEstudiantes(rawEst)
        : Array.isArray(rawEst)
          ? rawEst
          : [];

    let per = await api.getPeriodos();
    per = Array.isArray(per) ? per : [];
    periodosLista =
      typeof api.sortPeriodosRecientesPrimero === "function"
        ? api.sortPeriodosRecientesPrimero(per.slice())
        : per;

    const sel = $("gc-per");
    sel.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija período —";
    sel.appendChild(ph);
    periodosLista.forEach(function (p) {
      const o = document.createElement("option");
      o.value = p.id_periodo;
      o.textContent = p.nombre_periodo;
      sel.appendChild(o);
    });
    sel.value = "";
  }

  function resetWizardGc() {
    volActual = null;
    $("resumen-final").hidden = true;
    $("gc-sem").value = "";
    $("gc-mod").value = "";
    $("gc-msg").hidden = true;
    $("btn-gen-paso1").disabled = true;
    $("box-global").hidden = true;
    $("box-cred").hidden = true;
    $("gc-monto-global").textContent = "";
    $("gc-creds-sel").textContent = "0";
    $("gc-monto-cred").textContent = COP.format(0);
    $("gc-est").value = "";
    const fe = $("gc-filtro-est");
    if (fe) fe.value = "";
    $("gc-per").value = "";
    renderTablaEstudiantes();
  }

  function volanteYaExiste(idEst, idPer) {
    if (!idEst || !idPer) return Promise.resolve(false);
    return api.getVolantes({}).then(function (vols) {
      if (!Array.isArray(vols)) return false;
      return vols.some(function (v) {
        return Number(v.id_estudiante) === Number(idEst) && Number(v.id_periodo) === Number(idPer);
      });
    });
  }

  async function refrescarMontosPrincipal() {
    $("gc-msg").hidden = true;
    const idEst = Number($("gc-est").value);
    const idPer = Number($("gc-per").value);
    const semRaw = $("gc-sem").value;
    const mod = ($("gc-mod").value || "").trim();
    // El botón permanece deshabilitado durante TODA la validación
    $("btn-gen-paso1").disabled = true;
    $("box-global").hidden = true;
    $("box-cred").hidden = true;

    if (!idEst || !idPer || !mod || !semRaw) {
      return;
    }

    const semestre = Number(semRaw);
    if (!Number.isFinite(semestre)) return;

    // Mostrar indicador de verificación mientras se consulta
    $("gc-msg").textContent = "Verificando...";
    $("gc-msg").hidden = false;
    $("gc-msg").className = "alert";
    $("gc-msg").style.opacity = "0.7";

    const exists = await volanteYaExiste(idEst, idPer);
    $("gc-msg").style.opacity = "";
    if (exists) {
      $("gc-msg").textContent = "Este estudiante ya tiene volante en el período seleccionado.";
      $("gc-msg").hidden = false;
      $("gc-msg").className = "alert alert-error";
      return; // botón sigue disabled
    }
    $("gc-msg").hidden = true;

    let est = null;
    try {
      est = await api.getEstudiante(idEst);
    } catch (e) {
      $("gc-msg").textContent = "No se pudo cargar la información del estudiante.";
      $("gc-msg").hidden = false;
      $("gc-msg").className = "alert alert-error";
      return;
    }
    const rules = await api.getReglasCobro({ programa: est.id_programa, periodo: idPer });
    const regGlobal = rules.find(function (r) {
      return r.modalidad === "GLOBAL";
    });
    const regCred = rules.find(function (r) {
      return r.modalidad === "CREDITOS";
    });

    $('box-global').hidden = mod !== 'GLOBAL';
    $('box-cred').hidden = mod !== 'CREDITOS';

    if (mod === 'GLOBAL') {
      const v = regGlobal ? Number(regGlobal.valorglobal) : 0;
      $('gc-monto-global').textContent = COP.format(v);
      if (!regGlobal || v <= 0) {
        $('gc-msg').innerHTML =
          '<strong>Sin regla de cobro GLOBAL.</strong> No hay una regla de cobro GLOBAL ' +
          'configurada para el programa de este estudiante en el per\u00edodo seleccionado, ' +
          'o su valor es $\u00a00. Vaya a <em>Reglas de cobro</em> y cree la regla antes de generar el volante.';
        $('gc-msg').hidden = false;
        $('gc-msg').className = 'alert alert-error';
        return; // botón sigue disabled
      }
      // Todo validado: habilitar botón
      $('btn-gen-paso1').disabled = false;
    }

    if (mod === "CREDITOS") {
      const asig = await api.getAsignaturas({
        programa: est.id_programa,
        semestre: semestre,
      });
      const vc = regCred ? Number(regCred.valorcredito) : 0;
      $('gc-valor-credit').textContent = COP.format(vc);
      if (!regCred || vc <= 0) {
        $('gc-msg').innerHTML =
          '<strong>Sin regla de cobro por CR\u00c9DITOS.</strong> No hay una regla de cobro por CR\u00c9DITOS ' +
          'configurada para el programa de este estudiante en el per\u00edodo seleccionado, ' +
          'o su valor por cr\u00e9dito es $\u00a00. Vaya a <em>Reglas de cobro</em> y cree la regla antes de generar el volante.';
        $('gc-msg').hidden = false;
        $('gc-msg').className = 'alert alert-error';
        return; // botón sigue disabled
      }
      // Todo validado: habilitar botón (el usuario aún debe seleccionar asignaturas)
      $('btn-gen-paso1').disabled = false;
      const cont = $("gc-asig-list");
      cont.innerHTML = "";
      $("gc-creds-sel").textContent = "0";
      $("gc-monto-cred").textContent = COP.format(0);
      const asigList = Array.isArray(asig) ? asig : [];
      if (!asigList.length) {
        $('gc-msg').innerHTML =
          '<strong>Sin asignaturas disponibles.</strong> No hay asignaturas registradas en el cat\u00e1logo ' +
          'para el semestre ' + semestre + ' del programa de este estudiante. ' +
          'Vaya a <em>Asignaturas (cat\u00e1logo)</em> y agr\u00e9guelas antes de generar el volante.';
        $('gc-msg').hidden = false;
        $('gc-msg').className = 'alert alert-error';
        $('btn-gen-paso1').disabled = true;
        return;
      }
      asigList.forEach(function (a) {
        const row = document.createElement("div");
        row.className = "check-row";
        row.innerHTML =
          '<input type="checkbox" class="chk-a" id="ca' +
          a.id_asignatura +
          '" value="' +
          a.id_asignatura +
          '" data-creds="' +
          a.cant_creditos +
          '" />' +
          '<div class="check-body">' +
          "<label for='ca" +
          a.id_asignatura +
          "'>" +
          escapeHtml(a.nombre) +
          "</label><div style='font-size:0.85rem;color:var(--text-muted)'>" +
          a.cant_creditos +
          " créditos</div></div>";
        cont.appendChild(row);
      });
      cont.querySelectorAll(".chk-a").forEach(function (c) {
        c.addEventListener("change", recalcCred);
      });
    }
  }

  function recalcCred() {
    const idEst = Number($("gc-est").value);
    const idPer = Number($("gc-per").value);
    if (!idEst || !idPer) return;
    const checks = $("gc-asig-list").querySelectorAll(".chk-a:checked");
    let creds = 0;
    checks.forEach(function (c) {
      creds += Number(c.dataset.creds);
    });
    $("gc-creds-sel").textContent = String(creds);
    api
      .getEstudiante(idEst)
      .then(function (est) {
        return api.getReglasCobro({ programa: est.id_programa, periodo: idPer }).then(function (rules) {
          const regCred = rules.find(function (r) {
            return r.modalidad === "CREDITOS";
          });
          const valor = regCred ? regCred.valorcredito : 0;
          $("gc-monto-cred").textContent = COP.format(creds * valor);
        });
      })
      .catch(function () {});
  }

  async function generarPrincipal(ev) {
    ev.preventDefault();
    $("resumen-final").hidden = true;
    const idEst = Number($("gc-est").value);
    const idPer = Number($("gc-per").value);
    const semRaw = $("gc-sem").value;
    const modalidad = ($("gc-mod").value || "").trim();
    if (!idEst) {
      auth.showToast("Seleccione un estudiante en la tabla.", "error");
      return;
    }
    if (!idPer) {
      auth.showToast("Seleccione un período.", "error");
      return;
    }
    if (!semRaw) {
      auth.showToast("Seleccione el semestre a cobrar.", "error");
      return;
    }
    if (!modalidad) {
      auth.showToast("Seleccione la modalidad.", "error");
      return;
    }
    try {
      const semestre = Number(semRaw);
      let asignaturas = [];
      if (modalidad === "CREDITOS") {
        $("gc-asig-list").querySelectorAll(".chk-a:checked").forEach(function (c) {
          asignaturas.push(Number(c.value));
        });
        if (!asignaturas.length) {
          auth.showToast("Seleccione al menos una asignatura.", "error");
          return;
        }
      }

      volActual = await api.postVolante({
        id_estudiante: idEst,
        id_periodo: idPer,
        modalidad: modalidad,
        semestre_que_cobra: semestre,
        tipo_generacion: "INDIVIDUAL",
        asignaturas: asignaturas,
      });

      // Enriquecer con nombres usando los datos ya cargados en memoria
      const estSel = listaEstudiantesBase().find(function (e) {
        return Number(e.id_estudiante) === idEst;
      });
      // Leer el nombre del periodo directamente del texto de la opcion seleccionada
      const perSelectEl = $("gc-per");
      const perOpcion = perSelectEl ? perSelectEl.options[perSelectEl.selectedIndex] : null;
      const nombrePeriodo = (perOpcion && perOpcion.value) ? perOpcion.textContent.trim() : String(idPer);
      if (estSel) {
        volActual.nombre_estudiante = (estSel.nombre || "") + " " + (estSel.apellido || "");
        volActual.carnet = estSel.carnet || "";
        volActual.nombre_programa = estSel.nombre_programa || "";
      }
      volActual.nombre_periodo = nombrePeriodo;
      if (!volActual.estado) volActual.estado = "PENDIENTE";
      // Deshabilitar el botón inmediatamente: el volante ya existe
      $('btn-gen-paso1').disabled = true;
      $('gc-msg').textContent = 'Volante generado correctamente. Este estudiante ya tiene un volante en este per\u00edodo.';
      $('gc-msg').hidden = false;
      $('gc-msg').className = 'alert alert-success';
      auth.showToast("Volante principal creado.", "success");
      $('res-final-body').innerHTML = resumenHtml(volActual);
      $('resumen-final').hidden = false;
    } catch (err) {
      let msg = err.message || 'Error al generar el volante.';
      if (
        err.status === 409 ||
        msg.includes('ORA-00001') ||
        msg.includes('UQ_VOL_EST_PER') ||
        msg.includes('Otro usuario') ||
        msg.includes('Operaci\u00f3n duplicada') ||
        msg.includes('restricci\u00f3n \u00fanica')
      ) {
        msg =
          'Conflicto de acceso simultáneo: otro usuario generó el volante para este estudiante ' +
          'y período en el mismo instante. Recargue la página y verifique el estado del estudiante.';
        $('btn-gen-paso1').disabled = true;
        $('gc-msg').textContent = msg;
        $('gc-msg').hidden = false;
        $('gc-msg').className = 'alert alert-error';
      } else if (
        msg.includes('ORA-02291') ||
        msg.includes('FK_VOL_REGLA') ||
        msg.includes('clave principal no encontrada') ||
        msg.includes('parent key not found')
      ) {
        msg =
          'No se puede generar el volante: no existe una regla de cobro ' + modalidad +
          ' v\u00e1lida para el programa y per\u00edodo seleccionados. ' +
          'Vaya a \u201cReglas de cobro\u201d y configure la regla antes de intentarlo nuevamente.';
      } else if (msg.match(/ORA-\d+/) || msg.includes('violada') || msg.includes('restricci\u00f3n')) {
        msg =
          'Error en la base de datos al generar el volante. Verifique que exista una regla de cobro ' +
          modalidad + ' configurada para este programa y per\u00edodo.';
      }
      auth.showToast(msg, 'error');
    }
  }

  function resumenHtml(vol) {
    const nombreEst = vol.nombre_estudiante ? vol.nombre_estudiante.trim() : "(sin nombre)";
    const carnet = vol.carnet ? " · " + escapeHtml(vol.carnet) : "";
    const programa = vol.nombre_programa ? " · " + escapeHtml(vol.nombre_programa) : "";
    const periodo = vol.nombre_periodo || String(vol.id_periodo || "");
    const estado = vol.estado || "PENDIENTE";
    const badgeClass = "badge badge-" + estado.toLowerCase();
    return (
      "<p class='mb-0'>" +
      "<strong>Volante #" + escapeHtml(vol.id_volante) + "</strong>" +
      "<br /><strong>Estudiante:</strong> " + escapeHtml(nombreEst) + escapeHtml(carnet) + escapeHtml(programa) +
      "<br /><strong>Período:</strong> " + escapeHtml(periodo) +
      " &nbsp;<span class='" + badgeClass + "'>" + escapeHtml(estado) + "</span>" +
      "<br /><strong>Modalidad:</strong> " + escapeHtml(vol.modalidad || "") +
      " &nbsp;·&nbsp; <strong>Semestre cobrado:</strong> " + escapeHtml(vol.semestre_que_cobra || "") +
      "<br /><strong>Monto total (COBROS):</strong> " + COP.format(vol.monto_total || 0) +
      "</p>"
    );
  }

  async function initGenerarCobroPage() {
    bindGenerarCobroUi();
    try {
      await cargarCatalogos();
    } catch (err) {
      if (window.auth && typeof auth.showToast === "function") {
        auth.showToast(err.message || "Error al cargar catálogos", "error");
      }
    }
    renderTablaEstudiantes();
  }

  function boot() {
    if (!document.getElementById("gc-tbl-est")) return;
    if (window.__gcGenerarCobroInitDone) return;
    window.__gcGenerarCobroInitDone = true;
    void initGenerarCobroPage();
  }

  document.addEventListener("DOMContentLoaded", boot);
  if (document.readyState !== "loading") {
    boot();
  }
})();
