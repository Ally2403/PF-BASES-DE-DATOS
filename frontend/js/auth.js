const SESSION_KEY = "cce_sesion";

const NAV = [
  {
    label: "Dashboard",
    dash: "dashboard.html",
    perm: null,
    icon: "🏠",
    desc: "Vista general y accesos rápidos.",
  },
  {
    label: "Estudiantes",
    page: "estudiantes.html",
    perm: "GESTIONAR_ESTUDIANTES",
    icon: "👥",
    desc: "Administración de datos maestros de alumnos.",
  },
  {
    label: "Programas y planes",
    page: "programas.html",
    perm: "GESTIONAR_PROGRAMAS",
    icon: "🎓",
    desc: "Configuración de facultades, programas y mallas.",
  },
  {
    label: "Asignaturas (catálogo)",
    page: "asignaturas-catalogo.html",
    perm: "GESTIONAR_ASIGNATURAS",
    icon: "📚",
    desc: "Catálogo unificado de materias y créditos.",
  },
  {
    label: "Períodos",
    page: "periodos.html",
    perm: "GESTIONAR_PERIODOS",
    icon: "📅",
    desc: "Gestión de calendarios académicos.",
  },
  {
    label: "Reglas de cobro",
    page: "reglas-cobro.html",
    perm: "GESTIONAR_REGLAS",
    icon: "⚙️",
    desc: "Definición de algoritmos y tarifas de cobro.",
  },
  {
    label: "Códigos de detalle",
    page: "codigos-detalle.html",
    perm: "GESTIONAR_CODIGOS",
    icon: "🏷️",
    desc: "Diccionario de conceptos financieros.",
  },
  {
    label: "Generar cobro",
    page: "generar-cobro.html",
    perm: "GENERAR_COBRO_IND",
    icon: "📄",
    desc: "Creación de volantes de matrícula individuales.",
  },
  {
    label: "Cobros adicionales",
    page: "cobros-adicionales.html",
    perm: "COBROS_ADICIONALES",
    icon: "➕",
    desc: "Agregue cargos individuales a la cuenta corriente de un estudiante.",
  },
  {
    label: "Cobro masivo",
    page: "cobro-masivo.html",
    perm: "GENERAR_COBRO_MAS",
    icon: "📑",
    desc: "Generación automatizada por grupos.",
  },
  {
    label: "Cuenta corriente",
    page: "cuenta-corriente.html",
    perm: "VER_CUENTA",
    icon: "💳",
    desc: "Historial de cargos, pagos y saldos.",
  },
  {
    label: "Registrar pago",
    page: "registrar-pago.html",
    perm: "REGISTRAR_PAGO",
    icon: "💰",
    desc: "Legalización de ingresos por caja u online.",
  },
  {
    label: "Consultar pagos",
    page: "consultar-pagos.html",
    perm: "CONSULTAR_PAGOS",
    icon: "🔍",
    desc: "Búsqueda y detalle de transacciones realizadas.",
  },
  {
    label: "Reportes",
    page: "reportes.html",
    perm: "VER_REPORTES",
    icon: "📊",
    desc: "Análisis y exportación de datos.",
  },
  {
    label: "Usuarios",
    page: "usuarios.html",
    perm: "VER_USUARIOS",
    icon: "👤",
    desc: "Seguridad y control de acceso.",
  },
  {
    label: "Perfiles (Roles)",
    page: "perfiles.html",
    perm: "GESTIONAR_PERFILES",
    icon: "🛡️",
    desc: "Administración de roles y sus permisos.",
  },
];

function navHref(item) {
  const inPage = !!window.__IS_PAGE__;
  if (item.dash) return (inPage ? "../" : "") + item.dash;
  return (inPage ? "" : "pages/") + item.page;
}

function getSession() {
  try {
    const raw = sessionStorage.getItem(SESSION_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (_) {
    return null;
  }
}

function setSession(user) {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(user));
}

function clearSession() {
  sessionStorage.removeItem(SESSION_KEY);
}

function logout() {
  clearSession();
  const inPage = !!window.__IS_PAGE__;
  window.location.href = (inPage ? "../" : "") + "login.html";
}

function requireAuth() {
  const s = getSession();
  if (!s || !s.username) {
    const inPage = !!window.__IS_PAGE__;
    window.location.href = (inPage ? "../" : "") + "login.html";
  }
}

/** Un permiso o lista OR (cualquiera basta), alineado con `can` y el menú NAV */
function requirePerm(perm) {
  requireAuth();
  if (!can(perm)) {
    const inPage = !!window.__IS_PAGE__;
    window.location.href = (inPage ? "../" : "") + "dashboard.html";
  }
}

function can(perm) {
  const s = getSession();
  if (!perm) return true;
  if (Array.isArray(perm)) {
    return perm.some((p) => (s && s.permisos) ? s.permisos.includes(p) : false);
  }
  return (s && s.permisos) ? s.permisos.includes(perm) : false;
}

function renderSidebar(activeFile) {
  const sidebar = document.getElementById("sidebar-root");
  if (!sidebar) return;
  const s = getSession();
  if (!s) return;

  const items = NAV.filter((item) => {
    if (!item.perm) return true;
    return can(item.perm);
  });

  const navLi = items
    .map((item) => {
      const href = navHref(item);
      const fname = item.dash || item.page;
      const active = fname === activeFile ? " active" : "";
      return `<li><a class="${active.trim()}" href="${href}">${item.label}</a></li>`;
    })
    .join("");

  sidebar.innerHTML = `
    <div class="sidebar-header">
      <div class="sidebar-logo">Gestión Estudiantil</div>

    </div>
    <nav aria-label="Principal">
      <ul class="nav-menu">
        <li class="nav-section-title">Menú</li>
        ${navLi}
      </ul>
    </nav>
    <div class="sidebar-footer">
      <div class="user-chip">
        <strong>${escapeHtml(s.username)}</strong>
        <span>${escapeHtml(s.perfil || "")}</span>
      </div>
      <button type="button" class="btn btn-ghost" id="btn-logout">Cerrar sesión</button>
    </div>
  `.trim();

  const btn = document.getElementById("btn-logout");
  if (btn) btn.addEventListener("click", logout);
}

function escapeHtml(t) {
  const d = document.createElement("div");
  d.textContent = String(t ?? "");
  return d.innerHTML;
}

function ensureToastStack() {
  let el = document.getElementById("toast-stack");
  if (!el) {
    el = document.createElement("div");
    el.id = "toast-stack";
  }
  // Always move to end of body so it paints above modals regardless of backdrop-filter stacking context
  document.body.appendChild(el);
  return el;
}

function ensureAlertCenter() {
  let el = document.getElementById("alert-center-overlay");
  if (!el) {
    el = document.createElement("div");
    el.id = "alert-center-overlay";
  }
  // Always move to end of body so it paints above modals regardless of backdrop-filter stacking context
  document.body.appendChild(el);
  return el;
}

function showToast(message, kind) {
  kind = kind || "success";
  if (kind === "error") {
    // Errors appear centered on screen for 3 seconds
    const overlay = ensureAlertCenter();
    const div = document.createElement("div");
    div.className = "alert-center-msg error";
    div.textContent = message;
    overlay.appendChild(div);
    setTimeout(function() { div.classList.add("fade-out"); }, 2700);
    setTimeout(function() { div.remove(); }, 3100);
  } else {
    // Success stays bottom-right
    const stack = ensureToastStack();
    const div = document.createElement("div");
    div.className = "toast success";
    div.textContent = message;
    stack.appendChild(div);
    setTimeout(function() { div.remove(); }, 3200);
  }
}

function showAlert(message, title) {
  title = title || "Atención";
  var backdrop = document.createElement("div");
  backdrop.className = "modal-backdrop open";
  backdrop.style.background = "rgba(0,0,0,0.45)";
  backdrop.innerHTML =
    '<div class="modal-panel" style="width:min(420px,92%);text-align:center">' +
      '<div class="modal-header" style="justify-content:center;border-bottom:1px solid var(--border);padding-bottom:0.75rem;margin-bottom:1rem">' +
        '<h3 style="margin:0">⚠\uFE0F\u00A0' + title + '</h3>' +
      '</div>' +
      '<p style="margin:0;color:var(--text-muted);font-size:0.95rem">' + message + '</p>' +
    '</div>';
  document.body.appendChild(backdrop);
  function dismiss() {
    backdrop.style.transition = "opacity 0.3s";
    backdrop.style.opacity = "0";
    setTimeout(function() { backdrop.remove(); }, 320);
  }
  setTimeout(dismiss, 2200);
  backdrop.addEventListener("click", dismiss);
}

function showConfirm(message, title, confirmText, confirmClass) {
  title = title || "Confirmar eliminación";
  confirmText = confirmText || "Eliminar";
  confirmClass = confirmClass || "btn-danger";
  return new Promise(function (resolve) {
    var backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop open";
    backdrop.innerHTML =
      '<div class="modal-panel" style="width:min(400px,96%)">' +
        '<div class="modal-header"><h3>⚠\uFE0F\u00A0' + title + '</h3></div>' +
        '<p style="margin:0 0 1.5rem;color:var(--text-muted)">' + message + '</p>' +
        '<div class="btn-row" style="justify-content:flex-end;gap:0.6rem">' +
          '<button class="btn btn-secondary" data-action="cancel">Cancelar</button>' +
          '<button class="btn ' + confirmClass + '" data-action="ok">' + confirmText + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(backdrop);
    function close(result) { backdrop.remove(); resolve(result); }
    backdrop.addEventListener("click", function (e) {
      var a = e.target.closest("[data-action]");
      if (a) { close(a.dataset.action === "ok"); return; }
      if (e.target === backdrop) close(false);
    });
  });
}

/**
 * Diálogo de confirmación con verificación de cédula.
 * Muestra la acción, el impacto financiero y exige que el usuario
 * escriba su propia cédula antes de habilitar el botón de eliminar.
 *
 * @param {string} message   Descripción de lo que se va a eliminar.
 * @param {string} impacto   Advertencia sobre el efecto financiero/operativo.
 * @param {string} [title]   Título del diálogo (por defecto "Confirmar eliminación").
 * @returns {Promise<boolean>}
 */
function showConfirmCedula(message, impacto, title) {
  title = title || "Confirmar eliminación";
  var s = getSession();
  var cedulaEsperada = s && s.cedula ? String(s.cedula).trim() : "";

  return new Promise(function (resolve) {
    var backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop open";

    var impactoHtml = impacto
      ? '<div style="background:var(--warn-bg,#fff3cd);border-left:3px solid #f0ad4e;' +
        'padding:0.6rem 0.75rem;border-radius:4px;font-size:0.85rem;color:#7a5a00;' +
        'margin:0.75rem 0 1rem">' +
        '<strong>⚠\uFE0F Impacto:</strong> ' + impacto + '</div>'
      : '<div style="margin-bottom:1rem"></div>';

    var sinCedula = !cedulaEsperada;
    var cedulaLabel = sinCedula
      ? '<p style="font-size:0.8rem;color:var(--danger,#e74c3c);margin:0 0 0.5rem">' +
        'Su sesión no tiene cédula registrada. Contacte al administrador para completar su perfil.</p>'
      : '<label style="display:block;font-size:0.85rem;font-weight:600;margin-bottom:0.4rem">' +
        'Escriba su cédula para confirmar la eliminación:' +
        '</label>' +
        '<input type="text" id="_ced-inp" inputmode="numeric" autocomplete="off" maxlength="10" ' +
        'style="width:100%;box-sizing:border-box" placeholder="Ej. 1001234567" />' +
        '<div id="_ced-err" style="display:none;font-size:0.8rem;color:var(--danger,#e74c3c);margin-top:0.3rem">' +
        'Cédula incorrecta. Verifique e intente nuevamente.' +
        '</div>';

    backdrop.innerHTML =
      '<div class="modal-panel" style="width:min(480px,96%)">' +
        '<div class="modal-header"><h3>\uD83D\uDDD1\uFE0F\u00A0' + title + '</h3></div>' +
        '<p style="margin:0 0 0.25rem;color:var(--text-muted)">' + message + '</p>' +
        impactoHtml +
        '<div style="margin-bottom:1.25rem">' + cedulaLabel + '</div>' +
        '<div class="btn-row" style="justify-content:flex-end;gap:0.6rem">' +
          '<button class="btn btn-secondary" id="_ced-cancel">Cancelar</button>' +
          '<button class="btn btn-danger" id="_ced-ok"' + (sinCedula ? ' disabled' : ' disabled') + '>Eliminar definitivamente</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(backdrop);

    var inp = backdrop.querySelector("#_ced-inp");
    var btn = backdrop.querySelector("#_ced-ok");
    var errDiv = backdrop.querySelector("#_ced-err");

    function close(result) { backdrop.remove(); resolve(result); }

    backdrop.querySelector("#_ced-cancel").addEventListener("click", function () { close(false); });
    backdrop.addEventListener("click", function (e) { if (e.target === backdrop) close(false); });

    if (!sinCedula && inp) {
      inp.addEventListener("input", function () {
        btn.disabled = inp.value.trim() === "";
        if (errDiv) errDiv.style.display = "none";
      });
      inp.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !btn.disabled) btn.click();
      });
      setTimeout(function () { inp.focus(); }, 40);
    }

    btn.addEventListener("click", function () {
      if (sinCedula) { close(false); return; }
      if (inp.value.trim() === cedulaEsperada) {
        close(true);
      } else {
        if (errDiv) errDiv.style.display = "block";
        inp.value = "";
        btn.disabled = true;
        inp.focus();
      }
    });
  });
}

/**
 * @param {{ perm?: string | string[], activeFile?: string }} opts
 */
function initPage(opts) {
  opts = opts || {};
  if (opts.perm) requirePerm(opts.perm);
  else requireAuth();
  renderSidebar(opts.activeFile || "");
  // Refresh permisos from DB in the background on every page load
  _refreshPermisosBackground(opts.activeFile || "");
}

function _refreshPermisosBackground(activeFile) {
  var s = getSession();
  if (!s || !s.access_token) return;
  fetch("/api/auth/me", {
    headers: { "Authorization": "Bearer " + s.access_token }
  }).then(function(res) {
    if (!res.ok) return null;
    return res.json();
  }).then(function(data) {
    if (!data || !Array.isArray(data.permisos)) return;
    var updated = Object.assign({}, s, { permisos: data.permisos });
    setSession(updated);
    renderSidebar(activeFile);
  }).catch(function() {});
}

/* ── Bloqueo de caracteres inválidos en campos numéricos y teléfono ─── */
(function () {
  var BLOCKED_NUMBER = ["e", "E", "+", "-", ".", ","];
  var NAV_KEYS = ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Tab", "Home", "End"];

  document.addEventListener("keydown", function (ev) {
    var t = ev.target;
    if (t.tagName !== "INPUT") return;
    if (t.type === "number" && BLOCKED_NUMBER.indexOf(ev.key) !== -1) {
      ev.preventDefault();
    }
    if ((t.type === "tel" || t.getAttribute("inputmode") === "numeric") && NAV_KEYS.indexOf(ev.key) === -1 && !/^[0-9]$/.test(ev.key) && !ev.ctrlKey && !ev.metaKey) {
      ev.preventDefault();
    }
  }, true);

  document.addEventListener("input", function (ev) {
    var t = ev.target;
    if (t.tagName !== "INPUT") return;
    if (t.type === "tel" || t.getAttribute("inputmode") === "numeric") {
      var cleaned = t.value.replace(/[^0-9]/g, "");
      if (cleaned !== t.value) t.value = cleaned;
    }
    if (t.getAttribute("data-capitalize") === "words") {
      var start = t.selectionStart;
      var end = t.selectionEnd;
      var capped = t.value.replace(/(^|\s)\S/g, function (c) { return c.toUpperCase(); });
      if (capped !== t.value) {
        t.value = capped;
        t.setSelectionRange(start, end);
      }
    }
  }, true);
}());

window.auth = {
  SESSION_KEY,
  getSession,
  setSession,
  clearSession,
  logout,
  requireAuth,
  requirePerm,
  can,
  renderSidebar,
  showToast,
  showConfirm,
  showConfirmCedula,
  showAlert,
  initPage,
  navHref,
  NAV,
};
