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
    perm: ["GESTIONAR_ASIGNATURAS", "GESTIONAR_PROGRAMAS"],
    icon: "📚",
    desc: "Catálogo unificado de materias y créditos.",
  },
  {
    label: "Periodos",
    page: "periodos.html",
    perm: ["GESTIONAR_PROGRAMAS", "GESTIONAR_REGLAS"],
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
    perm: "GENERAR_COBRO_IND",
    icon: "➕",
    desc: "Cargos ad-hoc a cuenta corriente.",
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
    perm: "VER_REPORTES",
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
  {
    label: "Menús del sistema",
    page: "menus.html",
    perm: "GESTIONAR_MENUS",
    icon: "🛠️",
    desc: "Configuración de la estructura de navegación.",
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
      <div class="sidebar-meta">IST7111 · Universidad</div>
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
    document.body.appendChild(el);
  }
  return el;
}

function showToast(message, kind = "success") {
  const stack = ensureToastStack();
  const div = document.createElement("div");
  div.className = `toast ${kind === "error" ? "error" : "success"}`;
  div.textContent = message;
  stack.appendChild(div);
  setTimeout(() => div.remove(), 5200);
}

/**
 * @param {{ perm?: string | string[], activeFile?: string }} opts
 */
function initPage(opts) {
  opts = opts || {};
  if (opts.perm) requirePerm(opts.perm);
  else requireAuth();
  renderSidebar(opts.activeFile || "");
}

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
  initPage,
  navHref,
  NAV,
};
