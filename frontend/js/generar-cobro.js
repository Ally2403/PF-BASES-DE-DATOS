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
    $("gc-est").value = String(id);
    renderTablaEstudiantes();
    
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
    $("btn-gen-paso1").disabled = true;
    $("box-global").hidden = true;
    $("box-cred").hidden = true;

    if (!idEst || !idPer || !mod || !semRaw) {
      return;
    }

    const semestre = Number(semRaw);
    if (!Number.isFinite(semestre)) return;

    const exists = await volanteYaExiste(idEst, idPer);
    if (exists) {
      $("gc-msg").textContent = "Este estudiante ya tiene volante en el período seleccionado.";
      $("gc-msg").hidden = false;
      $("gc-msg").className = "alert alert-error";
      return;
    }

    $("btn-gen-paso1").disabled = false;

    let est = null;
    try {
      est = await api.getEstudiante(idEst);
    } catch (e) {
      return;
    }
    const rules = await api.getReglasCobro({ programa: est.id_programa, periodo: idPer });
    const regGlobal = rules.find(function (r) {
      return r.modalidad === "GLOBAL";
    });
    const regCred = rules.find(function (r) {
      return r.modalidad === "CREDITOS";
    });

    $("box-global").hidden = mod !== "GLOBAL";
    $("box-cred").hidden = mod !== "CREDITOS";

    if (mod === "GLOBAL") {
      const v = regGlobal ? regGlobal.valorglobal : 0;
      $("gc-monto-global").textContent = COP.format(v);
    }

    if (mod === "CREDITOS") {
      const asig = await api.getAsignaturas({
        programa: est.id_programa,
        semestre: semestre,
      });
      const vc = regCred ? regCred.valorcredito : 0;
      $("gc-valor-credit").textContent = COP.format(vc);
      const cont = $("gc-asig-list");
      cont.innerHTML = "";
      $("gc-creds-sel").textContent = "0";
      $("gc-monto-cred").textContent = COP.format(0);
      (Array.isArray(asig) ? asig : []).forEach(function (a) {
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
      auth.showToast("Volante principal creado.");
      $("res-final-body").innerHTML = resumenHtml(volActual);
      $("resumen-final").hidden = false;
    } catch (err) {
      auth.showToast(err.message || "Error", "error");
    }
  }

  function resumenHtml(vol) {
    return (
      "<p class='mb-0'><strong>Volante #" +
      vol.id_volante +
      "</strong> · " +
      escapeHtml(vol.nombre_estudiante) +
      "<br />Período " +
      escapeHtml(vol.nombre_periodo) +
      " · <span class='badge badge-" +
      String(vol.estado).toLowerCase() +
      "'>" +
      escapeHtml(vol.estado) +
      "</span><br /><strong>Monto total (COBROS):</strong> " +
      COP.format(vol.monto_total) +
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
