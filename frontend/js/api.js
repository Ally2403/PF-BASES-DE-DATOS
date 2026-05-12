/**
 * Capa única de acceso al backend FastAPI (Oracle).
 * Producción/mock: cambie solo USAR_MOCK cuando el servidor esté listo.
 */

const USAR_MOCK = false;

const API_BASE = "";

const MOCK_USERS = [
  {
    username: "cmendoza",
    nombre: "Carlos",
    apellido: "Mendoza",
    contrasena: "Admin123!",
    cedula: 101,
    correo: "cmendoza@uni.edu.co",
    telefono: "3001234567",
    id_user: 1,
    perfil: "ADMINISTRADOR",
    permisos: [
      "CREAR_USUARIO",
      "EDITAR_USUARIO",
      "ELIMINAR_USUARIO",
      "VER_USUARIOS",
      "GESTIONAR_PERFILES",
      "GESTIONAR_MENUS",
      "GESTIONAR_PROGRAMAS",
      "GESTIONAR_ASIGNATURAS",
      "GESTIONAR_ESTUDIANTES",
      "GESTIONAR_REGLAS",
      "GESTIONAR_CODIGOS",
      "GENERAR_COBRO_IND",
      "GENERAR_COBRO_MAS",
      "REGISTRAR_PAGO",
      "VER_CUENTA",
      "VER_REPORTES",
    ],
  },
  {
    username: "aperez",
    nombre: "Ana",
    apellido: "Pérez",
    contrasena: "Admin123!",
    cedula: 102,
    correo: "aperez@uni.edu.co",
    telefono: "3007654321",
    id_user: 2,
    perfil: "SUPERVISOR",
    permisos: [
      "GESTIONAR_PROGRAMAS",
      "GESTIONAR_ASIGNATURAS",
      "GESTIONAR_ESTUDIANTES",
      "GESTIONAR_REGLAS",
      "GESTIONAR_CODIGOS",
      "VER_REPORTES",
    ],
  },
  {
    username: "ltorres",
    nombre: "Luis",
    apellido: "Torres",
    contrasena: "Admin123!",
    cedula: 103,
    correo: "ltorres@uni.edu.co",
    telefono: "3000000000",
    id_user: 3,
    perfil: "ASISTENTE",
    permisos: ["GENERAR_COBRO_IND", "GENERAR_COBRO_MAS", "REGISTRAR_PAGO", "VER_CUENTA", "VER_REPORTES"],
  },
];

/** Semilla solo lectura; el mock muta una copia */
const MOCK_SEED = {
  estudiantes: [
    {
      id_estudiante: 1,
      carnet: "2026-SIS-001",
      nombre: "Maria",
      apellido: "Garcia",
      telefono: "3012345678",
      correo: "mgarcia@est.uni.edu.co",
      id_programa: 1,
      nombre_programa: "Ingeniería de Sistemas",
    },
    {
      id_estudiante: 2,
      carnet: "2026-SIS-002",
      nombre: "Pedro",
      apellido: "Lopez",
      telefono: "3023456789",
      correo: "plopez@est.uni.edu.co",
      id_programa: 1,
      nombre_programa: "Ingeniería de Sistemas",
    },
    {
      id_estudiante: 3,
      carnet: "2026-ADM-001",
      nombre: "Laura",
      apellido: "Ramirez",
      telefono: "3034567890",
      correo: "lramirez@est.uni.edu.co",
      id_programa: 2,
      nombre_programa: "Administración de Empresas",
    },
    {
      id_estudiante: 4,
      carnet: "2026-MED-001",
      nombre: "Andres",
      apellido: "Herrera",
      telefono: "3045678901",
      correo: "aherrera@est.uni.edu.co",
      id_programa: 3,
      nombre_programa: "Medicina",
    },
    {
      id_estudiante: 5,
      carnet: "2026-MED-002",
      nombre: "Juliana",
      apellido: "Castro",
      telefono: "3056789012",
      correo: "jcastro@est.uni.edu.co",
      id_programa: 3,
      nombre_programa: "Medicina",
    },
  ],

  programas: [
    { id_programa: 1, nombre_programa: "Ingeniería de Sistemas" },
    { id_programa: 2, nombre_programa: "Administración de Empresas" },
    { id_programa: 3, nombre_programa: "Medicina" },
  ],

  periodos: [
    { id_periodo: 1, nombre_periodo: "2026-10", fecha_inicio: "2026-01-15", fecha_fin: "2026-06-15" },
    { id_periodo: 2, nombre_periodo: "2026-20", fecha_inicio: "2026-07-15", fecha_fin: "2026-11-30" },
  ],

  reglas_cobro: [
    { modalidad: "GLOBAL", id_programa: 1, id_periodo: 1, valorglobal: 8500000, valorcredito: null },
    { modalidad: "CREDITOS", id_programa: 1, id_periodo: 1, valorglobal: null, valorcredito: 650000 },
    { modalidad: "GLOBAL", id_programa: 2, id_periodo: 1, valorglobal: 6500000, valorcredito: null },
    { modalidad: "CREDITOS", id_programa: 2, id_periodo: 1, valorglobal: null, valorcredito: 500000 },
    { modalidad: "GLOBAL", id_programa: 3, id_periodo: 1, valorglobal: 18000000, valorcredito: null },
    { modalidad: "CREDITOS", id_programa: 3, id_periodo: 1, valorglobal: null, valorcredito: 1400000 },
    { modalidad: "GLOBAL", id_programa: 1, id_periodo: 2, valorglobal: 8700000, valorcredito: null },
    { modalidad: "CREDITOS", id_programa: 1, id_periodo: 2, valorglobal: null, valorcredito: 670000 },
    { modalidad: "GLOBAL", id_programa: 2, id_periodo: 2, valorglobal: 6700000, valorcredito: null },
    { modalidad: "CREDITOS", id_programa: 2, id_periodo: 2, valorglobal: null, valorcredito: 520000 },
    { modalidad: "GLOBAL", id_programa: 3, id_periodo: 2, valorglobal: 18500000, valorcredito: null },
    { modalidad: "CREDITOS", id_programa: 3, id_periodo: 2, valorglobal: null, valorcredito: 1450000 },
  ],

  asignaturas_por_semestre: {
    "1-1": [
      { id_asignatura: 1, nombre: "Cálculo Diferencial", cant_creditos: 3 },
      { id_asignatura: 2, nombre: "Fundamentos de Programación", cant_creditos: 3 },
      { id_asignatura: 3, nombre: "Álgebra Lineal", cant_creditos: 3 },
      { id_asignatura: 5, nombre: "Física I", cant_creditos: 3 },
    ],
    "2-1": [
      { id_asignatura: 4, nombre: "Bases de Datos I", cant_creditos: 3 },
      { id_asignatura: 8, nombre: "Inglés I", cant_creditos: 2 },
    ],
    "1-2": [
      { id_asignatura: 6, nombre: "Contabilidad General", cant_creditos: 3 },
      { id_asignatura: 7, nombre: "Microeconomía", cant_creditos: 3 },
      { id_asignatura: 8, nombre: "Inglés I", cant_creditos: 2 },
    ],
    "2-2": [
      { id_asignatura: 1, nombre: "Cálculo Diferencial", cant_creditos: 3 },
      { id_asignatura: 8, nombre: "Inglés I", cant_creditos: 2 },
    ],
    "1-3": [
      { id_asignatura: 9, nombre: "Anatomía Humana", cant_creditos: 4 },
      { id_asignatura: 10, nombre: "Biología Celular", cant_creditos: 4 },
    ],
    "2-3": [
      { id_asignatura: 5, nombre: "Física I", cant_creditos: 3 },
      { id_asignatura: 8, nombre: "Inglés I", cant_creditos: 2 },
    ],
  },

  /** Catálogo ASIGNATURA (ID_ASIGNATURA, NOMBRE, CANT_CREDITOS) — mismo modelo que Oracle */
  asignaturas_catalogo: [
    { id_asignatura: 1, nombre: "Cálculo Diferencial", cant_creditos: 3 },
    { id_asignatura: 2, nombre: "Fundamentos de Programación", cant_creditos: 3 },
    { id_asignatura: 3, nombre: "Álgebra Lineal", cant_creditos: 3 },
    { id_asignatura: 4, nombre: "Bases de Datos I", cant_creditos: 3 },
    { id_asignatura: 5, nombre: "Física I", cant_creditos: 3 },
    { id_asignatura: 6, nombre: "Contabilidad General", cant_creditos: 3 },
    { id_asignatura: 7, nombre: "Microeconomía", cant_creditos: 3 },
    { id_asignatura: 8, nombre: "Inglés I", cant_creditos: 2 },
    { id_asignatura: 9, nombre: "Anatomía Humana", cant_creditos: 4 },
    { id_asignatura: 10, nombre: "Biología Celular", cant_creditos: 4 },
  ],

  /** Monto volante tras PMAT + cargos extras (consistente con movimientos) */
  volantes: [
    {
      id_volante: 1,
      id_estudiante: 1,
      nombre_estudiante: "Maria Garcia",
      id_programa: 1,
      id_periodo: 1,
      nombre_periodo: "2026-10",
      modalidad: "GLOBAL",
      semestre_que_cobra: 1,
      tipo_generacion: "INDIVIDUAL",
      monto_total: 8750000,
      estado: "PARCIAL",
      fecha_generacion: "2026-01-20",
    },
    {
      id_volante: 2,
      id_estudiante: 2,
      nombre_estudiante: "Pedro Lopez",
      id_programa: 1,
      id_periodo: 1,
      nombre_periodo: "2026-10",
      modalidad: "CREDITOS",
      semestre_que_cobra: 1,
      tipo_generacion: "INDIVIDUAL",
      monto_total: 7800000,
      estado: "PENDIENTE",
      fecha_generacion: "2026-01-21",
    },
  ],

  cuentas: [
    { id_cuenta: 1, id_estudiante: 1 },
    { id_cuenta: 2, id_estudiante: 2 },
  ],

  cuenta_movimientos: {},

  cobros_adicionales_disponibles: [
    { codigo_detalle: "PCAR", descripcion: "Carné digital", valor_sugerido: 50000 },
    { codigo_detalle: "PLAB", descripcion: "Laboratorios Médicos", valor_sugerido: 200000 },
    { codigo_detalle: "PEXA", descripcion: "Exámenes de ingreso", valor_sugerido: 150000 },
  ],

  codigos_detalle: [
    { codigo_detalle: "PMAT", grupo: "COBRO", descripcion: "Valor Global por programa", valor_defecto: null },
    { codigo_detalle: "PCRE", grupo: "COBRO", descripcion: "Valor crédito por programa", valor_defecto: null },
    { codigo_detalle: "PCAR", grupo: "COBRO", descripcion: "Carné digital", valor_defecto: 85000 },
    { codigo_detalle: "PLAB", grupo: "COBRO", descripcion: "Laboratorios Médicos", valor_defecto: 350000 },
    { codigo_detalle: "PEXA", grupo: "COBRO", descripcion: "Exámenes de ingreso", valor_defecto: 120000 },
    { codigo_detalle: "MPAG", grupo: "PAGO", descripcion: "Valor pagado para Matrícula", valor_defecto: null },
    { codigo_detalle: "ANT", grupo: "PAGO", descripcion: "Anticipo", valor_defecto: null },
    { codigo_detalle: "DESC", grupo: "PAGO", descripcion: "Descuento", valor_defecto: null },
    { codigo_detalle: "CRED", grupo: "PAGO", descripcion: "Crédito financiero", valor_defecto: null },
  ],

  reportes: null,

  usuarios: [
    {
      id_user: 1,
      username: "cmendoza",
      id_perfil: 1,
      nombre_perfil: "ADMINISTRADOR",
      cedula: 1001234567,
      nombre: "Carlos",
      apellido: "Mendoza",
      correo: "cmendoza@uni.edu.co",
    },
    {
      id_user: 2,
      username: "aperez",
      id_perfil: 2,
      nombre_perfil: "SUPERVISOR",
      cedula: 1002345678,
      nombre: "Ana",
      apellido: "Perez",
      correo: "aperez@uni.edu.co",
    },
    {
      id_user: 3,
      username: "ltorres",
      id_perfil: 3,
      nombre_perfil: "ASISTENTE",
      cedula: 1003456789,
      nombre: "Luis",
      apellido: "Torres",
      correo: "ltorres@uni.edu.co",
    },
  ],

  perfiles: [
    { id_perfil: 1, nombre_perfil: "ADMINISTRADOR" },
    { id_perfil: 2, nombre_perfil: "SUPERVISOR" },
    { id_perfil: 3, nombre_perfil: "ASISTENTE" },
  ],

  menus: [
    { id_menu: 1, nombre_funcion: "Dashboard", url_acceso: "/frontend/dashboard.html" },
    { id_menu: 2, nombre_funcion: "Estudiantes", url_acceso: "/frontend/pages/estudiantes.html" },
    { id_menu: 3, nombre_funcion: "Programas", url_acceso: "/frontend/pages/programas.html" },
  ],

  permisos_catalogo: [],
};

MOCK_SEED.cuenta_movimientos = {
  "1_1": [
    {
      id_mov: 1,
      fecha: "2026-01-20",
      codigo_detalle: "PMAT",
      descripcion_movimiento: "Valor Global por programa",
      grupo: "COBRO",
      debito: 8500000,
      credito: null,
      nota: null,
      id_volante: 1,
    },
    {
      id_mov: 3,
      fecha: "2026-01-20",
      codigo_detalle: "PCAR",
      descripcion_movimiento: "Carné digital",
      grupo: "COBRO",
      debito: 50000,
      credito: null,
      nota: null,
      id_volante: 1,
    },
    {
      id_mov: 4,
      fecha: "2026-01-20",
      codigo_detalle: "PLAB",
      descripcion_movimiento: "Laboratorios Médicos",
      grupo: "COBRO",
      debito: 200000,
      credito: null,
      nota: null,
      id_volante: 1,
    },
    {
      id_mov: 2,
      fecha: "2026-02-15",
      codigo_detalle: "MPAG",
      descripcion_movimiento: "Valor pagado para Matrícula",
      grupo: "PAGO",
      debito: null,
      credito: 4000000,
      nota: "Pago parcial caja",
      id_volante: 1,
    },
  ],
  "2_1": [
    {
      id_mov: 10,
      fecha: "2026-01-21",
      codigo_detalle: "PCRE",
      descripcion_movimiento: "Valor crédito por programa",
      grupo: "COBRO",
      debito: 7800000,
      credito: null,
      nota: null,
      id_volante: 2,
    },
  ],
};

MOCK_SEED.reportes = {
  listado_general: [
    {
      id_estudiante: 1,
      carnet: "2026-SIS-001",
      nombre_estudiante: "Maria",
      apellido_estudiante: "Garcia",
      nombre_programa: "Ingeniería de Sistemas",
      nombre_periodo: "2026-10",
      modalidad: "GLOBAL",
      semestre_que_cobra: 1,
      monto_total: 8750000,
      estado: "PARCIAL",
    },
    {
      id_estudiante: 2,
      carnet: "2026-SIS-002",
      nombre_estudiante: "Pedro",
      apellido_estudiante: "Lopez",
      nombre_programa: "Ingeniería de Sistemas",
      nombre_periodo: "2026-10",
      modalidad: "CREDITOS",
      semestre_que_cobra: 1,
      monto_total: 7800000,
      estado: "PENDIENTE",
    },
    {
      id_estudiante: 3,
      carnet: "2026-ADM-001",
      nombre_estudiante: "Laura",
      apellido_estudiante: "Ramirez",
      nombre_programa: "Administración de Empresas",
      nombre_periodo: "2026-10",
      modalidad: "GLOBAL",
      semestre_que_cobra: 1,
      monto_total: 6500000,
      estado: "PENDIENTE",
    },
    {
      id_estudiante: 4,
      carnet: "2026-MED-001",
      nombre_estudiante: "Andres",
      apellido_estudiante: "Herrera",
      nombre_programa: "Medicina",
      nombre_periodo: "2026-10",
      modalidad: "GLOBAL",
      semestre_que_cobra: 1,
      monto_total: 18000000,
      estado: "PENDIENTE",
    },
  ],
  ingreso_esperado: [
    {
      nombre_periodo: "2026-10",
      nombre_programa: "Ingeniería de Sistemas",
      modalidad: "GLOBAL",
      cantidad_volantes: 2,
      total_esperado: 17000000,
    },
    {
      nombre_periodo: "2026-10",
      nombre_programa: "Administración de Empresas",
      modalidad: "GLOBAL",
      cantidad_volantes: 1,
      valor_total_esperado: 6500000,
    },
    {
      nombre_periodo: "2026-10",
      nombre_programa: "Medicina",
      modalidad: "GLOBAL",
      cantidad_volantes: 2,
      valor_total_esperado: 36000000,
    },
  ],
  pendientes: [
    {
      id_estudiante: 1,
      carnet: "2026-SIS-001",
      nombre_estudiante: "Maria",
      apellido_estudiante: "Garcia",
      correo: "mgarcia@est.uni.edu.co",
      telefono: "3012345678",
      id_programa: 1,
      nombre_programa: "Ingeniería de Sistemas",
      nombre_periodo: "2026-10",
      id_volante: 1,
      modalidad: "GLOBAL",
      total_cobrado: 8750000,
      total_pagado: 4000000,
      saldo_pendiente: 4750000,
      estado: "PARCIAL",
    },
    {
      id_estudiante: 2,
      carnet: "2026-SIS-002",
      nombre_estudiante: "Pedro",
      apellido_estudiante: "Lopez",
      id_programa: 1,
      modalidad: "CREDITOS",
      total_cobrado: 7800000,
      total_pagado: 0,
      saldo_pendiente: 7800000,
      estado: "PENDIENTE",
    },
  ],
  ingreso_real: [
    {
      nombre_periodo: "2026-10",
      total_recaudado: 4000000,
    },
  ],
  cartera: [
    {
      id_estudiante: 4,
      carnet: "2026-MED-001",
      nombre_estudiante: "Andres",
      apellido_estudiante: "Herrera",
      correo: "aherrera@est.uni.edu.co",
      nombre_programa: "Medicina",
      nombre_periodo: "2026-10",
      valor_credito: 1400000,
    },
  ],
  transacciones: [],
};

function clone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Ordena períodos del más reciente al menos reciente.
 * Convención de nombre: AAAA-10 (1.ª mitad), AAAA-20 (intersemestral), AAAA-30 (2.ª mitad).
 * Mismo año: -30 antes que -20 antes que -10.
 */
function normalizarListaPeriodosRaw(raw) {
  if (Array.isArray(raw)) return raw;
  if (raw && Array.isArray(raw.data)) return raw.data;
  if (raw && Array.isArray(raw.periodos)) return raw.periodos;
  if (raw && Array.isArray(raw.items)) return raw.items;
  if (raw && Array.isArray(raw.results)) return raw.results;
  return [];
}

/** AAAA-10 / AAAA-20 / AAAA-30; mismo año: sufijo mayor = más reciente (30 > 20 > 10). */
function parseNombrePeriodoRecencia(p) {
  const nom = String(p.nombre_periodo || p.nombre || "").trim();
  let m = nom.match(/^(\d{4})\s*[-\u2013\u2212/]\s*(\d+)\s*$/);
  if (m) return { year: Number(m[1]), suf: Number(m[2]) };
  m = nom.match(/^(\d{4})(\d{2})$/);
  if (m) return { year: Number(m[1]), suf: Number(m[2]) };
  return null;
}

function sortPeriodosRecientesPrimero(periodos) {
  return [...periodos].sort(function (a, b) {
    const pa = parseNombrePeriodoRecencia(a);
    const pb = parseNombrePeriodoRecencia(b);
    if (pa && pb) {
      if (pb.year !== pa.year) return pb.year - pa.year;
      return pb.suf - pa.suf;
    }
    if (pa && !pb) return -1;
    if (!pa && pb) return 1;
    const fa = Date.parse(String(a.fecha_fin || "")) || 0;
    const fb = Date.parse(String(b.fecha_fin || "")) || 0;
    if (fb !== fa) return fb - fa;
    return Number(b.id_periodo || 0) - Number(a.id_periodo || 0);
  });
}

function normalizarListaEstudiantes(raw) {
  if (Array.isArray(raw)) return raw;
  if (raw && typeof raw === "object" && raw.id_estudiante != null && !Array.isArray(raw)) {
    return [raw];
  }
  if (raw && Array.isArray(raw.estudiantes)) return raw.estudiantes;
  if (raw && Array.isArray(raw.data)) return raw.data;
  if (raw && Array.isArray(raw.items)) return raw.items;
  if (raw && Array.isArray(raw.results)) return raw.results;
  return [];
}

function normalizarListaSimple(raw) {
  if (Array.isArray(raw)) return raw;
  if (raw && Array.isArray(raw.data)) return raw.data;
  if (raw && Array.isArray(raw.items)) return raw.items;
  if (raw && Array.isArray(raw.results)) return raw.results;
  return [];
}

let _mockStore = null;
let _next_MOV = 100;
let _next_TRANS = 500;
let _next_VOLANTE = 100;
let _next_ESTUDIANTE = 100;
let _next_CUENTA = 100;

function ensureCuenta(idEstudiante) {
  if (!_mockStore) return null;
  const id = Number(idEstudiante);
  let c = _mockStore.cuentas.find(x => Number(x.id_estudiante) === id);
  if (!c) {
    c = { id_cuenta: _next_CUENTA++, id_estudiante: id };
    _mockStore.cuentas.push(c);
  }
  return c;
}

function ensureMockStore() {
  if (!_mockStore) {
    _mockStore = clone(MOCK_SEED);
  }
  // Garantizar estructuras si faltan (por updates de codigo)
  if (!_mockStore.cuenta_movimientos) _mockStore.cuenta_movimientos = {};
  if (!_mockStore.transacciones) _mockStore.transacciones = [];
  if (!_mockStore.usuarios) _mockStore.usuarios = [...MOCK_USERS];
  
  // Sincronizar contadores de IDs
  const maxVol = Math.max(...(_mockStore.volantes || []).map((v) => v.id_volante || 0), 0);
  const maxEst = Math.max(...(_mockStore.estudiantes || []).map((e) => e.id_estudiante || 0), 0);
  const maxCue = Math.max(...(_mockStore.cuentas || []).map((c) => c.id_cuenta || 0), 0);
  const maxTrans = Math.max(...(_mockStore.transacciones || []).map((t) => t.id_transaccion || 0), 0);
  
  _next_VOLANTE = Math.max(_next_VOLANTE, maxVol + 1);
  _next_ESTUDIANTE = Math.max(_next_ESTUDIANTE, maxEst + 1);
  _next_CUENTA = Math.max(_next_CUENTA, maxCue + 1);
  _next_TRANS = Math.max(_next_TRANS, maxTrans + 1);

  Object.values(_mockStore.cuenta_movimientos || {}).forEach((arr) => {
    if (Array.isArray(arr)) {
      arr.forEach((m) => {
        if (m.id_mov >= _next_MOV) _next_MOV = m.id_mov + 1;
      });
    }
  });
}

function cuKey(idEst, idPer) {
  return `${idEst}_${idPer}`;
}

async function fetchJson(path, opts = {}) {
  const url = `${API_BASE}${path}`;
  
  // Construir headers con autenticación si está disponible
  const headers = {
    "Content-Type": "application/json",
    ...(opts.headers || {}),
  };
  
  // Agregar token de autenticación si existe
  const sessionStr = sessionStorage.getItem("cce_sesion");
  if (sessionStr) {
    try {
      const session = JSON.parse(sessionStr);
      if (session && session.access_token) {
        headers["Authorization"] = `Bearer ${session.access_token}`;
      }
    } catch (_) {
      // Ignorar errores al parsear sessionStorage
    }
  }
  
  const res = await fetch(url, {
    ...opts,
    headers,
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch (_) {
    data = { error: text || res.statusText };
  }
  if (!res.ok) {
    const err = new Error((data && data.error) || res.statusText || "Error HTTP");
    err.status = res.status;
    err.body = data;
    throw err;
  }
  return data;
}

/* ---------- API ---------- */

async function login({ username, contrasena }) {
  if (USAR_MOCK) {
    ensureMockStore();
    const u = MOCK_USERS.find(
      (x) =>
        String(x.username).toLowerCase() === String(username).toLowerCase() &&
        x.contrasena === contrasena,
    );
    if (!u) throw new Error("Usuario o contraseña incorrectos");
    return {
      id_user: u.id_user,
      username: u.username,
      nombre: u.nombre,
      apellido: u.apellido,
      perfil: u.perfil,
      permisos: [...u.permisos],
    };
  }
  const response = await fetchJson("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password: contrasena }),
  });
  // Retornar solo el user object (data), no el wrapper {success, message, data}
  return response.data;
}

/**
 * Listado de estudiantes. Filtro opcional alineado al modelo Oracle:
 * PK de ESTUDIANTE = ID_ESTUDIANTE (véase entregable3_ddl_final_final.sql).
 * Sin id_estudiante: el backend puede devolver el catálogo completo o paginado.
 */
async function getEstudiantes(params = {}) {
  const qp = new URLSearchParams();
  if (params.id_estudiante != null && String(params.id_estudiante).trim() !== "") {
    qp.set("id_estudiante", String(params.id_estudiante).trim());
  }
  const q = qp.toString();
  if (USAR_MOCK) {
    ensureMockStore();
    let list = [..._mockStore.estudiantes];
    if (params.id_estudiante != null && String(params.id_estudiante).trim() !== "") {
      const id = Number(params.id_estudiante);
      if (!Number.isFinite(id) || id < 1) {
        throw new Error("ID_ESTUDIANTE debe ser un entero válido (clave primaria).");
      }
      list = list.filter((e) => Number(e.id_estudiante) === id);
    }
    return list;
  }
  const raw = await fetchJson(q ? `/api/estudiantes?${q}` : "/api/estudiantes");
  return normalizarListaEstudiantes(raw);
}

async function getEstudiante(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    const e = _mockStore.estudiantes.find((x) => String(x.id_estudiante) === String(id));
    if (!e) throw new Error("Estudiante no encontrado");
    return e;
  }
  return fetchJson(`/api/estudiantes/${id}`);
}

async function postEstudiante(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const dup = _mockStore.estudiantes.some((e) => e.carnet === body.carnet || e.correo === body.correo);
    if (dup) throw new Error("Carné o correo ya existe");
    const prog = _mockStore.programas.find((p) => p.id_programa === body.id_programa);
    const nuevo = {
      id_estudiante: _next_ESTUDIANTE++,
      nombre_programa: prog ? prog.nombre_programa : "",
      ...body,
    };
    _mockStore.estudiantes.push(nuevo);
    return nuevo;
  }
  return fetchJson("/api/estudiantes", { method: "POST", body: JSON.stringify(body) });
}

async function putEstudiante(id, body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.estudiantes.findIndex((x) => String(x.id_estudiante) === String(id));
    if (i < 0) throw new Error("Estudiante no encontrado");
    const prog =
      body.id_programa !== undefined
        ? _mockStore.programas.find((p) => p.id_programa === body.id_programa)
        : null;
    Object.assign(_mockStore.estudiantes[i], body);
    if (prog) _mockStore.estudiantes[i].nombre_programa = prog.nombre_programa;
    return _mockStore.estudiantes[i];
  }
  return fetchJson(`/api/estudiantes/${id}`, { method: "PUT", body: JSON.stringify(body) });
}

async function deleteEstudiante(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.estudiantes.findIndex((x) => String(x.id_estudiante) === String(id));
    if (i < 0) throw new Error("Estudiante no encontrado");
    _mockStore.estudiantes.splice(i, 1);
    return { ok: true };
  }
  return fetchJson(`/api/estudiantes/${id}`, { method: "DELETE" });
}

async function getProgramas(params = {}) {
  const qp = new URLSearchParams();
  if (params.id_programa != null && String(params.id_programa).trim() !== "") {
    qp.set("id_programa", String(params.id_programa).trim());
  }
  const q = qp.toString();
  if (USAR_MOCK) {
    ensureMockStore();
    let list = [..._mockStore.programas];
    if (params.id_programa != null && String(params.id_programa).trim() !== "") {
      const id = Number(params.id_programa);
      if (!Number.isFinite(id) || id < 1) {
        throw new Error("ID_PROGRAMA debe ser un entero válido.");
      }
      list = list.filter((p) => Number(p.id_programa) === id);
    }
    return list;
  }
  const raw = await fetchJson(q ? `/api/programas?${q}` : "/api/programas");
  return normalizarListaSimple(raw);
}

async function postPrograma(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const nombre = String(body.nombre_programa || "").trim();
    if (!nombre) throw new Error("Nombre obligatorio");
    const id =
      Math.max(..._mockStore.programas.map((p) => p.id_programa), 0) + 1;
    const row = { id_programa: id, nombre_programa: nombre };
    _mockStore.programas.push(row);
    return row;
  }
  return fetchJson("/api/programas", { method: "POST", body: JSON.stringify(body) });
}

async function putPrograma(id, body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.programas.findIndex((p) => String(p.id_programa) === String(id));
    if (i < 0) throw new Error("Programa no encontrado");
    if (body.nombre_programa) _mockStore.programas[i].nombre_programa = String(body.nombre_programa).trim();
    _mockStore.estudiantes.forEach((e) => {
      if (e.id_programa === _mockStore.programas[i].id_programa) {
        e.nombre_programa = _mockStore.programas[i].nombre_programa;
      }
    });
    return _mockStore.programas[i];
  }
  return fetchJson(`/api/programas/${id}`, { method: "PUT", body: JSON.stringify(body) });
}

async function deletePrograma(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.programas.findIndex((p) => String(p.id_programa) === String(id));
    if (i < 0) throw new Error("Programa no encontrado");
    const progId = _mockStore.programas[i].id_programa;
    const uso = _mockStore.estudiantes.some((e) => Number(e.id_programa) === Number(progId));
    if (uso) throw new Error("No se puede eliminar: programa referenciado por estudiantes.");
    if (_mockStore.reglas_cobro.some((r) => Number(r.id_programa) === Number(progId))) {
      throw new Error("No se puede eliminar: existen reglas de cobro para este programa.");
    }
    if (_mockStore.volantes.some((v) => Number(v.id_programa) === Number(progId))) {
      throw new Error("No se puede eliminar: existen volantes asociados a este programa.");
    }
    for (let s = 1; s <= 10; s++) {
      delete _mockStore.asignaturas_por_semestre[`${s}-${progId}`];
    }
    _mockStore.programas.splice(i, 1);
    return { ok: true };
  }
  return fetchJson(`/api/programas/${id}`, { method: "DELETE" });
}

function planKey(semestre, idPrograma) {
  return `${Number(semestre)}-${Number(idPrograma)}`;
}

function syncPeaCopiesFromCatalog(idAsignatura) {
  const cat = _mockStore.asignaturas_catalogo.find(
    (c) => Number(c.id_asignatura) === Number(idAsignatura),
  );
  if (!cat) return;
  Object.keys(_mockStore.asignaturas_por_semestre).forEach((key) => {
    const arr = _mockStore.asignaturas_por_semestre[key];
    arr.forEach((row, idx) => {
      if (Number(row.id_asignatura) === Number(idAsignatura)) {
        arr[idx] = {
          id_asignatura: cat.id_asignatura,
          nombre: cat.nombre,
          cant_creditos: cat.cant_creditos,
        };
      }
    });
  });
}

function removeAsignaturaFromAllPlans(idAsignatura) {
  Object.keys(_mockStore.asignaturas_por_semestre).forEach((key) => {
    _mockStore.asignaturas_por_semestre[key] = _mockStore.asignaturas_por_semestre[key].filter(
      (row) => Number(row.id_asignatura) !== Number(idAsignatura),
    );
  });
}

async function getCatalogoAsignaturas() {
  if (USAR_MOCK) {
    ensureMockStore();
    return [..._mockStore.asignaturas_catalogo].sort((a, b) =>
      Number(a.id_asignatura) - Number(b.id_asignatura),
    );
  }
  const raw = await fetchJson("/api/asignaturas");
  return normalizarListaSimple(raw);
}

async function postAsignaturaCatalog(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const nombre = String(body.nombre || "").trim();
    const cc = Number(body.cant_creditos);
    if (!nombre) throw new Error("NOMBRE obligatorio.");
    if (!Number.isFinite(cc) || cc < 1 || cc > 10) {
      throw new Error("CANT_CREDITOS debe estar entre 1 y 10.");
    }
    const next =
      Math.max(..._mockStore.asignaturas_catalogo.map((a) => Number(a.id_asignatura)), 0) + 1;
    const row = { id_asignatura: next, nombre, cant_creditos: cc };
    _mockStore.asignaturas_catalogo.push(row);
    return row;
  }
  return fetchJson("/api/asignaturas", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

async function putAsignaturaCatalog(id, body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.asignaturas_catalogo.findIndex(
      (a) => String(a.id_asignatura) === String(id),
    );
    if (i < 0) throw new Error("Asignatura no encontrada.");
    if (body.nombre != null) {
      _mockStore.asignaturas_catalogo[i].nombre = String(body.nombre).trim();
    }
    if (body.cant_creditos != null) {
      const cc = Number(body.cant_creditos);
      if (!Number.isFinite(cc) || cc < 1 || cc > 10) {
        throw new Error("CANT_CREDITOS debe estar entre 1 y 10.");
      }
      _mockStore.asignaturas_catalogo[i].cant_creditos = cc;
    }
    syncPeaCopiesFromCatalog(id);
    return _mockStore.asignaturas_catalogo[i];
  }
  return fetchJson(`/api/asignaturas/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deleteAsignaturaCatalog(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.asignaturas_catalogo.findIndex(
      (a) => String(a.id_asignatura) === String(id),
    );
    if (i < 0) throw new Error("Asignatura no encontrada.");
    removeAsignaturaFromAllPlans(id);
    _mockStore.asignaturas_catalogo.splice(i, 1);
    return { ok: true };
  }
  return fetchJson(`/api/asignaturas/${id}`, { method: "DELETE" });
}

/** PLAN_ESTUDIO en mock: existe fila si hay clave semestre-id_programa en asignaturas_por_semestre */
async function postPlanEstudioSemestre(id_programa, semestre) {
  const pid = Number(id_programa);
  const sem = Number(semestre);
  if (!Number.isFinite(pid) || pid < 1) throw new Error("ID_PROGRAMA inválido.");
  if (!Number.isFinite(sem) || sem < 1 || sem > 10) {
    throw new Error("SEMESTRE debe estar entre 1 y 10.");
  }
  if (USAR_MOCK) {
    ensureMockStore();
    const prog = _mockStore.programas.some((p) => Number(p.id_programa) === pid);
    if (!prog) throw new Error("Programa no existe.");
    const k = planKey(sem, pid);
    if (!_mockStore.asignaturas_por_semestre[k]) _mockStore.asignaturas_por_semestre[k] = [];
    return { semestre: sem, id_programa: pid };
  }
  return fetchJson(`/api/programas/${pid}/planes`, {
    method: "POST",
    body: JSON.stringify({ semestre: sem }),
  });
}

async function deletePlanEstudioSemestre(id_programa, semestre) {
  const pid = Number(id_programa);
  const sem = Number(semestre);
  if (USAR_MOCK) {
    ensureMockStore();
    delete _mockStore.asignaturas_por_semestre[planKey(sem, pid)];
    return { ok: true };
  }
  throw new Error("Eliminar semestres del plan no está habilitado en este backend.");
}

async function postPlanEstudioAsignatura(id_programa, semestre, id_asignatura) {
  const pid = Number(id_programa);
  const sem = Number(semestre);
  const aid = Number(id_asignatura);
  if (USAR_MOCK) {
    ensureMockStore();
    const k = planKey(sem, pid);
    if (!_mockStore.asignaturas_por_semestre[k]) {
      throw new Error("Primero agregue el semestre al plan (PLAN_ESTUDIO).");
    }
    const cat = _mockStore.asignaturas_catalogo.find((a) => Number(a.id_asignatura) === aid);
    if (!cat) throw new Error("ID_ASIGNATURA no existe en el catálogo.");
    const arr = _mockStore.asignaturas_por_semestre[k];
    if (arr.some((x) => Number(x.id_asignatura) === aid)) {
      throw new Error("La asignatura ya está en ese semestre.");
    }
    arr.push({
      id_asignatura: cat.id_asignatura,
      nombre: cat.nombre,
      cant_creditos: cat.cant_creditos,
    });
    return { semestre: sem, id_programa: pid, id_asignatura: aid };
  }
  return fetchJson(`/api/programas/${pid}/planes/${sem}/asignaturas`, {
    method: "POST",
    body: JSON.stringify({ id_asignatura: aid }),
  });
}

async function deletePlanEstudioAsignatura(id_programa, semestre, id_asignatura) {
  const pid = Number(id_programa);
  const sem = Number(semestre);
  const aid = Number(id_asignatura);
  if (USAR_MOCK) {
    ensureMockStore();
    const k = planKey(sem, pid);
    const arr = _mockStore.asignaturas_por_semestre[k];
    if (!arr) throw new Error("Semestre no existe en el plan.");
    _mockStore.asignaturas_por_semestre[k] = arr.filter((x) => Number(x.id_asignatura) !== aid);
    return { ok: true };
  }
  throw new Error("Quitar asignaturas del plan no está habilitado en este backend.");
}

async function getPeriodos(params = {}) {
  if (USAR_MOCK) {
    ensureMockStore();
    let r = sortPeriodosRecientesPrimero([..._mockStore.periodos]);
    if (params.id_periodo != null && String(params.id_periodo).trim() !== "") {
      r = r.filter((x) => String(x.id_periodo) === String(params.id_periodo));
    }
    return r;
  }
  const q = new URLSearchParams(params).toString();
  const raw = await fetchJson(q ? `/api/periodos?${q}` : "/api/periodos");
  let r = normalizarListaPeriodosRaw(raw);
  if (params.id_periodo != null && String(params.id_periodo).trim() !== "") {
    r = r.filter((x) => String(x.id_periodo) === String(params.id_periodo));
  }
  return sortPeriodosRecientesPrimero(r);
}

async function postPeriodo(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const nom = String(body.nombre_periodo || "").trim();
    const ini = body.fecha_inicio;
    const fin = body.fecha_fin;
    if (!nom || !ini || !fin) throw new Error("Todos los campos son obligatorios");
    const id =
      Math.max(..._mockStore.periodos.map((p) => p.id_periodo), 0) + 1;
    const row = { id_periodo: id, nombre_periodo: nom, fecha_inicio: ini, fecha_fin: fin };
    _mockStore.periodos.push(row);
    return row;
  }
  return fetchJson("/api/periodos", { method: "POST", body: JSON.stringify(body) });
}

async function putPeriodo(id, body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.periodos.findIndex((p) => String(p.id_periodo) === String(id));
    if (i < 0) throw new Error("Periodo no encontrado");
    Object.assign(_mockStore.periodos[i], body);
    return _mockStore.periodos[i];
  }
  return fetchJson(`/api/periodos/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deletePeriodo(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.periodos.findIndex((p) => String(p.id_periodo) === String(id));
    if (i < 0) throw new Error("Periodo no encontrado");
    const pid = _mockStore.periodos[i].id_periodo;
    if (_mockStore.volantes.some((v) => Number(v.id_periodo) === Number(pid))) {
      throw new Error("No se puede eliminar: existen volantes para este periodo.");
    }
    if (_mockStore.reglas_cobro.some((r) => Number(r.id_periodo) === Number(pid))) {
      throw new Error("No se puede eliminar: existen reglas de cobro para este periodo.");
    }
    _mockStore.periodos.splice(i, 1);
    return { ok: true };
  }
  return fetchJson(`/api/periodos/${id}`, { method: "DELETE" });
}

async function getReglasCobro(params = {}) {
  const idPrograma = Number(params.programa || params.id_programa);
  const idPeriodo = Number(params.periodo || params.id_periodo);

  function mapRegla(r) {
    return {
      modalidad: r.modalidad,
      id_programa: r.id_programa,
      id_periodo: r.id_periodo,
      valor_global: r.valor_global,
      valor_credito: r.valor_credito,
      valorglobal: r.valorglobal ?? r.valor_global ?? null,
      valorcredito: r.valorcredito ?? r.valor_credito ?? null,
    };
  }

  if (USAR_MOCK) {
    ensureMockStore();
    let r = [..._mockStore.reglas_cobro];
    if (params.programa) r = r.filter((x) => String(x.id_programa) === String(params.programa));
    if (params.periodo) r = r.filter((x) => String(x.id_periodo) === String(params.periodo));
    return r;
  }

  if (idPrograma && idPeriodo) {
    const raw = await fetchJson(`/api/programas/${idPrograma}/periodos/${idPeriodo}/reglas`);
    return normalizarListaSimple(raw).map(mapRegla);
  }

  const programas = await getProgramas();
  const periodos = await getPeriodos();
  const combinaciones = [];
  programas.forEach(function (p) {
    periodos.forEach(function (per) {
      combinaciones.push({ id_programa: p.id_programa, id_periodo: per.id_periodo });
    });
  });

  const resultados = await Promise.all(
    combinaciones.map(async function (c) {
      try {
        const raw = await fetchJson(`/api/programas/${c.id_programa}/periodos/${c.id_periodo}/reglas`);
        return normalizarListaSimple(raw).map(mapRegla);
      } catch (_) {
        return [];
      }
    }),
  );

  return resultados.flat();
}

function findReglaIndex(id_programa, id_periodo, modalidad) {
  const m = String(modalidad || "").toUpperCase();
  return _mockStore.reglas_cobro.findIndex(
    (x) =>
      Number(x.id_programa) === Number(id_programa) &&
      Number(x.id_periodo) === Number(id_periodo) &&
      String(x.modalidad).toUpperCase() === m,
  );
}

async function postReglaCobro(body) {
  const pid = Number(body.id_programa);
  const per = Number(body.id_periodo);
  const mod = String(body.modalidad || "").toUpperCase();
  if (!pid || !per || (mod !== "GLOBAL" && mod !== "CREDITOS")) {
    throw new Error("Programa, periodo y modalidad (GLOBAL | CREDITOS) son obligatorios.");
  }
  if (USAR_MOCK) {
    ensureMockStore();
    if (findReglaIndex(pid, per, mod) >= 0) {
      throw new Error("Ya existe una regla para ese programa, periodo y modalidad.");
    }
    const vg = body.valorglobal != null ? Number(body.valorglobal) : null;
    const vc = body.valorcredito != null ? Number(body.valorcredito) : null;
    if (mod === "GLOBAL" && (vg == null || !Number.isFinite(vg) || vg < 0)) {
      throw new Error("Valor global obligatorio y válido para modalidad GLOBAL.");
    }
    if (mod === "CREDITOS" && (vc == null || !Number.isFinite(vc) || vc < 0)) {
      throw new Error("Valor crédito obligatorio y válido para modalidad CREDITOS.");
    }
    const row = {
      modalidad: mod,
      id_programa: pid,
      id_periodo: per,
      valorglobal: mod === "GLOBAL" ? vg : null,
      valorcredito: mod === "CREDITOS" ? vc : null,
    };
    _mockStore.reglas_cobro.push(row);
    return row;
  }
  const payload = {
    modalidad: mod,
    valor_global: mod === "GLOBAL" ? Number(body.valorglobal) : null,
    valor_credito: mod === "CREDITOS" ? Number(body.valorcredito) : null,
  };
  return fetchJson(`/api/programas/${pid}/periodos/${per}/reglas`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

async function putReglaCobro(id_programa, id_periodo, modalidad, body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = findReglaIndex(id_programa, id_periodo, modalidad);
    if (i < 0) throw new Error("Regla no encontrada.");
    const mod = String(_mockStore.reglas_cobro[i].modalidad).toUpperCase();
    if (body.valorglobal != null) {
      const vg = Number(body.valorglobal);
      if (!Number.isFinite(vg) || vg < 0) throw new Error("Valor global inválido.");
      _mockStore.reglas_cobro[i].valorglobal = mod === "GLOBAL" ? vg : null;
    }
    if (body.valorcredito != null) {
      const vc = Number(body.valorcredito);
      if (!Number.isFinite(vc) || vc < 0) throw new Error("Valor crédito inválido.");
      _mockStore.reglas_cobro[i].valorcredito = mod === "CREDITOS" ? vc : null;
    }
    return _mockStore.reglas_cobro[i];
  }
  throw new Error("Actualizar reglas no está habilitado en este backend.");
}

async function deleteReglaCobro(id_programa, id_periodo, modalidad) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = findReglaIndex(id_programa, id_periodo, modalidad);
    if (i < 0) throw new Error("Regla no encontrada.");
    _mockStore.reglas_cobro.splice(i, 1);
    return { ok: true };
  }
  throw new Error("Eliminar reglas no está habilitado en este backend.");
}

function codigoDetalleEnUsoEnMock(cod) {
  const c = String(cod);
  const extras = _mockStore.cobros_adicionales_disponibles || [];
  if (extras.some((x) => x.codigo_detalle === c)) {
    return true;
  }
  const cm = _mockStore.cuenta_movimientos || {};
  return Object.keys(cm).some((k) => (cm[k] || []).some((m) => m.codigo_detalle === c));
}

async function getCodigosDetalle() {
  if (USAR_MOCK) {
    ensureMockStore();
    return [..._mockStore.codigos_detalle].sort((a, b) =>
      String(a.codigo_detalle).localeCompare(String(b.codigo_detalle)),
    );
  }
  const raw = await fetchJson("/api/codigos");
  return normalizarListaSimple(raw);
}

async function postCodigoDetalle(body) {
  const cod = String(body.codigo_detalle || "")
    .trim()
    .toUpperCase();
  const grupo = String(body.grupo || "")
    .trim()
    .toUpperCase();
  const descripcion = String(body.descripcion || "").trim();
  const valor_defecto = body.valor_defecto ? Number(body.valor_defecto) : null;
  if (!cod || cod.length < 2 || cod.length > 20) {
    throw new Error("Código inválido (2–20 caracteres).");
  }
  if (grupo !== "COBRO" && grupo !== "PAGO") {
    throw new Error("Grupo debe ser COBRO o PAGO.");
  }
  if (!descripcion) throw new Error("Descripción obligatoria.");
  if (USAR_MOCK) {
    ensureMockStore();
    if (_mockStore.codigos_detalle.some((x) => x.codigo_detalle === cod)) {
      throw new Error("Ya existe ese código de detalle.");
    }
    const row = { codigo_detalle: cod, grupo, descripcion, valor_defecto };
    _mockStore.codigos_detalle.push(row);
    return row;
  }
  return fetchJson("/api/codigos", { method: "POST", body: JSON.stringify(body) });
}

async function putCodigoDetalle(codigo, body) {
  const key = String(codigo || "").trim().toUpperCase();
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.codigos_detalle.findIndex((x) => x.codigo_detalle === key);
    if (i < 0) throw new Error("Código no encontrado.");
    if (body.grupo != null) {
      const g = String(body.grupo).trim().toUpperCase();
      if (g !== "COBRO" && g !== "PAGO") throw new Error("Grupo debe ser COBRO o PAGO.");
      _mockStore.codigos_detalle[i].grupo = g;
    }
    if (body.descripcion != null) {
      _mockStore.codigos_detalle[i].descripcion = String(body.descripcion).trim();
    }
    if (body.valor_defecto !== undefined) {
      _mockStore.codigos_detalle[i].valor_defecto = body.valor_defecto ? Number(body.valor_defecto) : null;
    }
    return _mockStore.codigos_detalle[i];
  }
  return fetchJson(`/api/codigos/${encodeURIComponent(key)}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deleteCodigoDetalle(codigo) {
  const key = String(codigo || "").trim().toUpperCase();
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.codigos_detalle.findIndex((x) => x.codigo_detalle === key);
    if (i < 0) throw new Error("Código no encontrado.");
    if (codigoDetalleEnUsoEnMock(key)) {
      throw new Error("No se puede eliminar: el código está referenciado (mock).");
    }
    _mockStore.codigos_detalle.splice(i, 1);
    return { ok: true };
  }
  return fetchJson(`/api/codigos-detalle/${encodeURIComponent(key)}`, { method: "DELETE" });
}

async function getAsignaturas(params = {}) {
  const sem = Number(params.semestre);
  const prog = Number(params.programa);
  if (USAR_MOCK) {
    ensureMockStore();
    const key = `${sem}-${prog}`;
    return [...(_mockStore.asignaturas_por_semestre[key] || [])];
  }
  if (!Number.isFinite(sem) || !Number.isFinite(prog)) return [];
  const raw = await fetchJson(`/api/programas/${prog}/planes/${sem}/asignaturas`);
  return normalizarListaSimple(raw);
}

async function getPlanPorPrograma(id_programa) {
  const pid = Number(id_programa);
  if (!Number.isFinite(pid) || pid < 1) return [];
  if (USAR_MOCK) return getPlanPorProgramaMock(pid);

  const rawPlanes = await fetchJson(`/api/programas/${pid}/planes`);
  const planes = normalizarListaSimple(rawPlanes);
  const bloques = await Promise.all(
    planes.map(async function (p) {
      const sem = Number(p.semestre);
      const rawAsig = await fetchJson(`/api/programas/${pid}/planes/${sem}/asignaturas`);
      return {
        semestre: sem,
        asignaturas: normalizarListaSimple(rawAsig),
      };
    }),
  );
  return bloques;
}

function getPlanPorProgramaMock(id_programa) {
  ensureMockStore();
  const pid = Number(id_programa);
  const out = [];
  for (let s = 1; s <= 10; s++) {
    const key = `${s}-${pid}`;
    const list = _mockStore.asignaturas_por_semestre[key];
    if (list) out.push({ semestre: s, asignaturas: clone(list) });
  }
  return out;
}

function findRegla(programaId, periodoId, modalidad) {
  return _mockStore.reglas_cobro.find(
    (r) =>
      r.id_programa === programaId && r.id_periodo === periodoId && r.modalidad === modalidad,
  );
}

async function postVolante(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const {
      id_estudiante,
      id_periodo,
      modalidad,
      semestre_que_cobra,
      tipo_generacion,
      asignaturas = [],
    } = body;
    const exists = _mockStore.volantes.some(
      (v) =>
        Number(v.id_estudiante) === Number(id_estudiante) &&
        Number(v.id_periodo) === Number(id_periodo),
    );
    if (exists) throw new Error("El estudiante ya tiene volante en este período");
    const est = _mockStore.estudiantes.find((e) => Number(e.id_estudiante) === Number(id_estudiante));
    if (!est) throw new Error("Estudiante no encontrado");
    const per = _mockStore.periodos.find((p) => Number(p.id_periodo) === Number(id_periodo));
    if (!per) throw new Error("Periodo inválido");
    const regla = findRegla(est.id_programa, Number(id_periodo), modalidad);
    if (!regla) throw new Error("No hay regla de cobro para programa, período y modalidad");
    let montoMatricula = 0;
    let codigoPrincipal = "PMAT";
    if (modalidad === "GLOBAL") {
      montoMatricula = regla.valorglobal;
      codigoPrincipal = "PMAT";
    } else {
      codigoPrincipal = "PCRE";
      const lista = clone(
        _mockStore.asignaturas_por_semestre[`${semestre_que_cobra}-${est.id_programa}`] || [],
      );
      const ids = new Set(asignaturas.map(Number));
      let creditos = 0;
      lista.forEach((a) => {
        if (ids.has(a.id_asignatura)) creditos += a.cant_creditos;
      });
      montoMatricula = creditos * regla.valorcredito;
      if (!montoMatricula) throw new Error("Seleccione asignaturas para modalidad CREDITOS");
    }
    const nombre_estudiante = `${est.nombre} ${est.apellido}`;
    const vol = {
      id_volante: _next_VOLANTE++,
      id_estudiante: est.id_estudiante,
      nombre_estudiante,
      id_periodo: Number(id_periodo),
      nombre_periodo: per.nombre_periodo,
      modalidad,
      semestre_que_cobra: Number(semestre_que_cobra),
      tipo_generacion: tipo_generacion || "INDIVIDUAL",
      monto_total: montoMatricula,
      estado: "PENDIENTE",
      fecha_generacion: new Date().toISOString().slice(0, 10),
      id_programa: est.id_programa,
    };
    _mockStore.volantes.push(vol);
    ensureCuenta(est.id_estudiante);
    const key = cuKey(est.id_estudiante, id_periodo);
    if (!_mockStore.cuenta_movimientos[key]) _mockStore.cuenta_movimientos[key] = [];
    const cdPri = _mockStore.codigos_detalle.find(function (c) {
      return c.codigo_detalle === codigoPrincipal;
    });
    const descPrincipal = cdPri ? cdPri.descripcion : codigoPrincipal;
    _mockStore.cuenta_movimientos[key].push({
      id_mov: _next_MOV++,
      fecha: vol.fecha_generacion,
      codigo_detalle: codigoPrincipal,
      descripcion_movimiento: descPrincipal,
      grupo: "COBRO",
      debito: montoMatricula,
      credito: null,
      nota: null,
      id_volante: vol.id_volante,
    });
    syncReportListadoFromVolantes();
    return clone(vol);
  }
  const raw = await fetchJson("/api/asistente/volantes/individual", {
    method: "POST",
    body: JSON.stringify(body),
  });
  return raw && raw.data ? raw.data : raw;
}

function syncReportListadoFromVolantes() {
  const periodoNombre = {};
  _mockStore.periodos.forEach((p) => {
    periodoNombre[p.id_periodo] = p.nombre_periodo;
  });
  _mockStore.reportes.listado_general = _mockStore.volantes.map((v) => {
    const e = _mockStore.estudiantes.find((x) => x.id_estudiante === v.id_estudiante);
    return {
      id_estudiante: v.id_estudiante,
      carnet: e ? e.carnet : "",
      nombre_estudiante: e ? e.nombre : "",
      apellido_estudiante: e ? e.apellido : "",
      nombre_programa: e ? e.nombre_programa : "",
      nombre_periodo: v.nombre_periodo,
      modalidad: v.modalidad,
      semestre_que_cobra: v.semestre_que_cobra,
      monto_total: v.monto_total,
      estado: v.estado,
    };
  });
}

async function postVolantesMasivo(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const { id_periodo, id_programa, modalidad, semestre } = body;
    const periodoNum = Number(id_periodo);
    const programaNum = Number(id_programa);
    if (!programaNum || !periodoNum) throw new Error("Programa y período son obligatorios");
    if (modalidad === "CREDITOS") {
      throw new Error(
        "Masivo CREDITOS: no definido en mock (acordar con backend: asignaturas por estudiante o solo GLOBAL)",
      );
    }
    const ests = _mockStore.estudiantes.filter((e) => e.id_programa === programaNum);
    const creados = [];
    let omitidos = 0;
    const regla = findRegla(programaNum, periodoNum, "GLOBAL");
    if (!regla) throw new Error("Sin regla GLOBAL para ese programa/período");
    for (const est of ests) {
      const exists = _mockStore.volantes.some(
        (v) => Number(v.id_estudiante) === est.id_estudiante && Number(v.id_periodo) === periodoNum,
      );
      if (exists) {
        omitidos++;
        continue;
      }
      const vol = await postVolante({
        id_estudiante: est.id_estudiante,
        id_periodo: periodoNum,
        modalidad: "GLOBAL",
        semestre_que_cobra: Number(semestre || 1),
        tipo_generacion: "MASIVA",
        asignaturas: [],
      });
      creados.push(vol);
    }
    return { ok: true, creados: creados.length, omitidos, detalle: creados };
  }
  const raw = await fetchJson("/api/asistente/volantes/masiva", {
    method: "POST",
    body: JSON.stringify(body),
  });
  const payload = raw && raw.data ? raw.data : raw;
  return {
    ...payload,
    creados: payload && payload.cantidad != null ? payload.cantidad : 0,
  };
}

async function postCobroAdicional(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const { id_volante, id_estudiante, id_periodo, codigo_detalle, valor, descripcion } = body;
    const allowed = ["PCAR", "PLAB", "PEXA"];
    if (!allowed.includes(codigo_detalle))
      throw new Error("Solo se permiten cobros adicionales PCAR, PLAB o PEXA");
    const valorNum = Number(valor);
    if (!valorNum || valorNum <= 0) throw new Error("Valor inválido");
    ensureCuenta(id_estudiante);
    const key = cuKey(id_estudiante, id_periodo);
    if (!_mockStore.cuenta_movimientos[key]) _mockStore.cuenta_movimientos[key] = [];
    const cdrow = _mockStore.codigos_detalle.find((c) => c.codigo_detalle === codigo_detalle);
    _mockStore.cuenta_movimientos[key].push({
      id_mov: _next_MOV++,
      fecha: new Date().toISOString().slice(0, 10),
      codigo_detalle,
      descripcion_movimiento:
        descripcion || (cdrow ? cdrow.descripcion : codigo_detalle),
      grupo: "COBRO",
      debito: valorNum,
      credito: null,
      nota: null,
      id_volante: id_volante ? Number(id_volante) : null,
    });
    
    if (id_volante) {
      const vol = _mockStore.volantes.find((v) => Number(v.id_volante) === Number(id_volante));
      if (vol) recalcularEstadoVolante(vol);
    }
    syncReportListadoFromVolantes();
    return { ok: true };
  }
  return fetchJson("/api/asistente/cobros-adicionales", { method: "POST", body: JSON.stringify(body) });
}

async function deleteMovimiento(id_mov) {
  if (USAR_MOCK) {
    ensureMockStore();
    const id = Number(id_mov);
    let found = false;
    for (const key in _mockStore.cuenta_movimientos) {
      const idx = _mockStore.cuenta_movimientos[key].findIndex((m) => m.id_mov === id);
      if (idx !== -1) {
        const mov = _mockStore.cuenta_movimientos[key][idx];
        // Si es cobro de matricula y tiene volante, eliminar el volante para permitir regenerar
        if (mov.id_volante && (mov.codigo_detalle === "PMAT" || mov.codigo_detalle === "PCRE")) {
          _mockStore.volantes = _mockStore.volantes.filter((v) => v.id_volante !== mov.id_volante);
        }
        _mockStore.cuenta_movimientos[key].splice(idx, 1);
        found = true;
        break;
      }
    }
    if (!found) throw new Error("Movimiento no encontrado");
    return { ok: true };
  }
  return fetchJson("/api/cuenta-corriente/movimientos/" + id_mov, { method: "DELETE" });
}

function computeSaldo(rows, est, nombrePeriodo, idPeriodo) {
  let totalCobros = 0,
    totalPagos = 0;
  rows.forEach((m) => {
    if (m.grupo === "COBRO" && m.debito != null) totalCobros += Number(m.debito);
    if (m.grupo === "PAGO" && m.credito != null) totalPagos += Number(m.credito);
  });
  const saldo = totalCobros - totalPagos;
  const nombreCompleto =
    `${est?.nombre ?? ""} ${est?.apellido ?? ""}`.trim();
  return {
    id_estudiante: Number(est?.id_estudiante),
    estudiante: nombreCompleto || "—",
    id_periodo: Number(idPeriodo),
    nombre_periodo: nombrePeriodo || "—",
    total_cobros: totalCobros,
    total_pagos: totalPagos,
    saldo_neto: saldo,
  };
}

async function getCuentaCorriente(params = {}) {
  const est = Number(params.estudiante);
  const per = Number(params.periodo);
  if (USAR_MOCK) {
    ensureMockStore();
    const key = cuKey(est, per);
    const list = [...(_mockStore.cuenta_movimientos[key] || [])];
    // Enriquecer con descripción del catálogo
    return list.map(m => {
        const det = _mockStore.codigos_detalle.find(d => d.codigo_detalle === m.codigo_detalle);
        return {
            ...m,
            descripcion_movimiento: det ? det.descripcion : (m.codigo_detalle || '—')
        };
    });
  }
  const raw = await fetchJson(`/api/cuenta-corriente/${est}`);
  let movs = normalizarListaSimple(raw);
  if (per) {
    const periodos = await getPeriodos({ id_periodo: per });
    const nombrePeriodo = periodos.length ? periodos[0].nombre_periodo : null;
    if (nombrePeriodo) {
      movs = movs.filter(function (m) {
        return String(m.nombre_periodo) === String(nombrePeriodo);
      });
    }
  }
  return movs;
}

async function getSaldo(params = {}) {
  const est = Number(params.estudiante);
  const per = Number(params.periodo);
  if (USAR_MOCK) {
    ensureMockStore();
    const key = cuKey(est, per);
    const rows = [...(_mockStore.cuenta_movimientos[key] || [])];
    const estudiante = _mockStore.estudiantes.find((e) => Number(e.id_estudiante) === est);
    const periodoObj = _mockStore.periodos.find((p) => Number(p.id_periodo) === per);
    return computeSaldo(
      rows,
      estudiante,
      periodoObj ? periodoObj.nombre_periodo : "",
      per,
    );
  }
  const raw = await fetchJson(`/api/cuenta-corriente/${est}/saldo`);
  const saldos = normalizarListaSimple(raw);
  if (!per) return saldos[0] || null;
  return (
    saldos.find(function (s) {
      return Number(s.id_periodo) === per;
    }) || {
      id_estudiante: est,
      id_periodo: per,
      total_cobros: 0,
      total_pagos: 0,
      saldo_neto: 0,
      nombre_periodo: "",
      estudiante: "",
    }
  );
}

function recalcularEstadoVolante(vol) {
  const key = cuKey(vol.id_estudiante, vol.id_periodo);
  const rows = _mockStore.cuenta_movimientos[key] || [];
  let cob = 0;
  let pag = 0;
  rows.forEach((m) => {
    if (Number(m.id_volante) !== Number(vol.id_volante)) return;
    if (m.grupo === "COBRO" && m.debito != null) cob += Number(m.debito);
    if (m.grupo === "PAGO" && m.credito != null) pag += Number(m.credito);
  });
  vol.monto_total = cob;
  if (pag <= 0) vol.estado = "PENDIENTE";
  else if (pag < cob) vol.estado = "PARCIAL";
  else vol.estado = "PAGADO";
}

async function postPago(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const { id_estudiante, id_volante, id_mov_cargo, id_periodo, medio_pago, referencia, valor_pagado, codigo_detalle } = body;
    const val = Number(valor_pagado);
    if (!val || val <= 0) throw new Error("Valor de pago inválido");
    if (!codigo_detalle) throw new Error("Código de detalle de pago obligatorio");

    const key = cuKey(id_estudiante, id_periodo);
    if (!_mockStore.cuenta_movimientos[key]) _mockStore.cuenta_movimientos[key] = [];

    const vol = _mockStore.volantes.find(v => Number(v.id_estudiante) === Number(id_estudiante) && Number(v.id_periodo) === Number(id_periodo));
    
    const refKey = `${medio_pago}|${String(referencia || "").trim() || Date.now()}`;
    const duplicado =
      medio_pago === "SIMULADO_ONLINE" ? false :
      (_mockStore.cuenta_movimientos[key].some((m) => m.codigo_detalle === codigo_detalle && m.ref_key === refKey));
    if (duplicado) throw new Error("Ya existe un registro con esta referencia y medio para este concepto");

    const movPago = {
      id_mov: _next_MOV++,
      fecha: new Date().toISOString().slice(0, 10),
      codigo_detalle: codigo_detalle,
      grupo: "PAGO",
      debito: null,
      credito: val,
      // Si es pago de matricula o hay un volante, lo vinculamos para el reporte
      id_volante: vol ? Number(vol.id_volante) : null,
      id_mov_asociado: id_mov_cargo ? Number(id_mov_cargo) : null,
      ref_key: refKey,
    };
    _mockStore.cuenta_movimientos[key].push(movPago);

    // Persistir en tabla transacciones para busqueda posterior
    const est = _mockStore.estudiantes.find(e => Number(e.id_estudiante) === Number(id_estudiante));
    const det = _mockStore.codigos_detalle.find(d => d.codigo_detalle === codigo_detalle);
    _mockStore.transacciones.push({
        id_transaccion: _next_TRANS++,
        referencia: referencia || "N/A",
        medio_pago,
        fecha_pago: movPago.fecha,
        id_mov: movPago.id_mov,
        carnet_estudiante: est ? est.carnet : "N/A",
        nombre_estudiante: est ? `${est.nombre} ${est.apellido}` : "Desconocido",
        concepto_pago: det ? det.descripcion : codigo_detalle
    });

    if (vol) {
      recalcularEstadoVolante(vol);
    }
    syncReportListadoFromVolantes();
    return movPago;
  }
  const volantes = await getVolantes({
    id_estudiante: body.id_estudiante,
    id_periodo: body.id_periodo,
  });
  const vol = Array.isArray(volantes) && volantes.length ? volantes[0] : null;
  if (!vol || !vol.id_volante) {
    throw new Error("No existe volante para ese estudiante y período.");
  }

  return fetchJson("/api/asistente/pagos", {
    method: "POST",
    body: JSON.stringify({
      id_volante: vol.id_volante,
      medio_pago: body.medio_pago,
      valor: body.valor_pagado,
      referencia: body.referencia || null,
    }),
  });
}

async function getPagos(filtros = {}) {
  if (USAR_MOCK) {
    ensureMockStore();
    let rows = [...(_mockStore.transacciones || [])];
    
    // Simular VW_CONSULTA_PAGOS (Join con Movimiento y Codigo Detalle)
    rows = rows.map(t => {
        let valor = 0;
        let det = _mockStore.codigos_detalle.find(d => d.codigo_detalle === t.codigo_detalle);
        let concepto = t.concepto_pago || "Pago";
        
        // Buscar el movimiento original
        for (const k in _mockStore.cuenta_movimientos) {
            const m = _mockStore.cuenta_movimientos[k].find(x => x.id_mov === t.id_mov);
            if (m) {
                valor = m.credito;
                break;
            }
        }
        return { 
            ...t, 
            valor_pagado: valor, 
            nombre_estudiante: t.estudiante // Alineado con la vista
        };
    });

    if (filtros.referencia) {
        const ref = filtros.referencia.toLowerCase();
        rows = rows.filter(r => String(r.referencia).toLowerCase().includes(ref));
    }
    if (filtros.medio_pago) {
        rows = rows.filter(r => r.medio_pago === filtros.medio_pago);
    }
    if (filtros.carnet) {
        const c = filtros.carnet.toLowerCase();
        rows = rows.filter(r => String(r.carnet).toLowerCase().includes(c));
    }
    return rows;
  }
  const raw = await fetchJson(`/api/reportes/consulta-pagos`);
  let rows = normalizarListaSimple(raw).map(function (r) {
    return {
      ...r,
      concepto_pago: r.concepto,
    };
  });

  if (filtros.referencia) {
    const ref = String(filtros.referencia).toLowerCase();
    rows = rows.filter((r) => String(r.referencia || "").toLowerCase().includes(ref));
  }
  if (filtros.medio_pago) {
    rows = rows.filter((r) => String(r.medio_pago || "") === String(filtros.medio_pago));
  }
  if (filtros.carnet) {
    const c = String(filtros.carnet).toLowerCase();
    rows = rows.filter((r) => String(r.carnet || "").toLowerCase().includes(c));
  }
  return rows;
}

async function getMovimientosPendientes(id_estudiante, id_periodo) {
  if (USAR_MOCK) {
    ensureMockStore();
    const key = cuKey(id_estudiante, id_periodo);
    const movs = _mockStore.cuenta_movimientos[key] || [];
    return movs.filter(m => m.grupo === "COBRO").map(m => {
        const det = _mockStore.codigos_detalle.find(d => d.codigo_detalle === m.codigo_detalle);
        return {
            id_mov: m.id_mov,
            descripcion: det ? det.descripcion : m.codigo_detalle,
            valor: m.debito,
            id_volante: m.id_volante
        };
    });
  }
  const movs = await getCuentaCorriente({ estudiante: id_estudiante, periodo: id_periodo });
  return movs
    .filter((m) => m.grupo === "COBRO")
    .map((m) => ({
      id_mov: m.id_mov,
      descripcion: m.descripcion_movimiento,
      valor: m.debito,
      id_volante: m.id_volante || null,
    }));
}

async function reporteListadoGeneral(periodo) {
  if (USAR_MOCK) {
    ensureMockStore();
    syncReportListadoFromVolantes();
    let rows = [..._mockStore.reportes.listado_general];
    if (periodo) rows = rows.filter((r) => {
      const p = _mockStore.periodos.find((x) => String(x.id_periodo) === String(periodo));
      return !p || r.nombre_periodo === p.nombre_periodo;
    });
    return rows;
  }
  const raw = await fetchJson(`/api/reportes/listado-estudiantes`);
  let rows = normalizarListaSimple(raw);
  if (periodo) {
    const per = await getPeriodos({ id_periodo: periodo });
    const nom = per.length ? per[0].nombre_periodo : null;
    if (nom) rows = rows.filter((r) => String(r.nombre_periodo) === String(nom));
  }
  return rows;
}

async function reporteIngresoEsperado(periodo) {
  if (USAR_MOCK) {
    ensureMockStore();
    // Simular suma de cobros por periodo y programa
    let results = {};
    Object.keys(_mockStore.cuenta_movimientos).forEach(key => {
        const [idEst, idPer] = key.split('_');
        if (periodo && String(idPer) !== String(periodo)) return;
        
        const est = _mockStore.estudiantes.find(e => String(e.id_estudiante) === idEst);
        const per = _mockStore.periodos.find(p => String(p.id_periodo) === idPer);
        if (!est || !per) return;

        const groupKey = `${per.nombre_periodo}|${est.nombre_programa}`;
        if (!results[groupKey]) results[groupKey] = { nombre_periodo: per.nombre_periodo, nombre_programa: est.nombre_programa, cantidad_estudiantes: 0, total_esperado: 0 };
        
        const cobros = _mockStore.cuenta_movimientos[key].filter(m => m.grupo === 'COBRO');
        if (cobros.length > 0) {
            results[groupKey].cantidad_estudiantes++;
            results[groupKey].total_esperado += cobros.reduce((s, m) => s + Number(m.debito || 0), 0);
        }
    });
    return Object.values(results);
  }
  const raw = await fetchJson(`/api/reportes/ingreso-esperado`);
  let rows = normalizarListaSimple(raw);
  if (periodo) {
    const per = await getPeriodos({ id_periodo: periodo });
    const nom = per.length ? per[0].nombre_periodo : null;
    if (nom) rows = rows.filter((r) => String(r.nombre_periodo) === String(nom));
  }
  return rows;
}

async function reportePendientes(programa, periodo) {
  if (USAR_MOCK) {
    ensureMockStore();
    let rows = [..._mockStore.reportes.pendientes];
    const pid = Number(programa);
    rows = rows.filter((r) => Number(r.id_programa) === pid);
    if (periodo) {
      const p = _mockStore.periodos.find((x) => String(x.id_periodo) === String(periodo));
      if (p) rows = rows.filter((r) => r.nombre_periodo === p.nombre_periodo);
    }
    return rows;
  }
  const q = new URLSearchParams();
  if (programa) q.set("id_programa", String(programa));
  const raw = await fetchJson(`/api/reportes/pendientes-pago${q.toString() ? `?${q.toString()}` : ""}`);
  let rows = normalizarListaSimple(raw);
  if (periodo) {
    const per = await getPeriodos({ id_periodo: periodo });
    const nom = per.length ? per[0].nombre_periodo : null;
    if (nom) rows = rows.filter((r) => String(r.nombre_periodo) === String(nom));
  }
  return rows;
}

async function reporteIngresoReal() {
  if (USAR_MOCK) {
    ensureMockStore();
    let results = {};
    Object.keys(_mockStore.cuenta_movimientos).forEach(key => {
        const [_, idPer] = key.split('_');
        const per = _mockStore.periodos.find(p => String(p.id_periodo) === idPer);
        if (!per) return;

        if (!results[per.nombre_periodo]) results[per.nombre_periodo] = { nombre_periodo: per.nombre_periodo, total_recaudado: 0 };
        
        const pagos = _mockStore.cuenta_movimientos[key].filter(m => m.grupo === 'PAGO');
        results[per.nombre_periodo].total_recaudado += pagos.reduce((s, m) => s + Number(m.credito || 0), 0);
    });
    // Ordenar por nombre de periodo DESC (2026-30 > 2026-10)
    return Object.values(results).sort((a, b) => b.nombre_periodo.localeCompare(a.nombre_periodo));
  }
  const raw = await fetchJson(`/api/reportes/ingreso-real`);
  return normalizarListaSimple(raw);
}

async function reporteCartera(periodo) {
  if (USAR_MOCK) {
    ensureMockStore();
    let rows = [..._mockStore.reportes.cartera];
    if (periodo) {
      const p = _mockStore.periodos.find((x) => String(x.id_periodo) === String(periodo));
      if (p) rows = rows.filter((r) => r.nombre_periodo === p.nombre_periodo);
    }
    return rows;
  }
  const raw = await fetchJson(`/api/reportes/cartera`);
  let rows = normalizarListaSimple(raw);
  if (periodo) {
    const per = await getPeriodos({ id_periodo: periodo });
    const nom = per.length ? per[0].nombre_periodo : null;
    if (nom) rows = rows.filter((r) => String(r.nombre_periodo) === String(nom));
  }
  return rows;
}

async function getUsuarios() {
  if (USAR_MOCK) {
    ensureMockStore();
    return [..._mockStore.usuarios];
  }
  const raw = await fetchJson("/api/usuarios");
  return normalizarListaSimple(raw);
}

async function postUsuario(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    if (_mockStore.usuarios.some((u) => u.username === body.username || u.cedula === Number(body.cedula)))
      throw new Error("Username o cédula duplicados");
    const perf = _mockStore.perfiles.find((p) => p.id_perfil === body.id_perfil);
    const nuevo = {
      id_user: Math.max(..._mockStore.usuarios.map((u) => u.id_user), 0) + 1,
      username: body.username,
      contrasena: body.contrasena || "Admin123!",
      id_perfil: Number(body.id_perfil),
      nombre_perfil: perf ? perf.nombre_perfil : "?",
      cedula: Number(body.cedula),
      nombre: body.nombre || "Nuevo",
      apellido: body.apellido || "",
      correo: body.correo || "",
      telefono: body.telefono || "",
    };
    _mockStore.usuarios.push(nuevo);
    return nuevo;
  }
  return fetchJson("/api/usuarios", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

async function putUsuario(id, body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.usuarios.findIndex((u) => String(u.id_user) === String(id));
    if (i < 0) throw new Error("Usuario no encontrado");
    Object.assign(_mockStore.usuarios[i], body);
    if (body.id_perfil) {
      const perf = _mockStore.perfiles.find((p) => p.id_perfil === body.id_perfil);
      if (perf) _mockStore.usuarios[i].nombre_perfil = perf.nombre_perfil;
    }
    return _mockStore.usuarios[i];
  }
  return fetchJson(`/api/usuarios/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deleteUsuario(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    const i = _mockStore.usuarios.findIndex((u) => String(u.id_user) === String(id));
    if (i < 0) throw new Error("Usuario no encontrado");
    _mockStore.usuarios.splice(i, 1);
    return { ok: true };
  }
  return fetchJson(`/api/usuarios/${id}`, { method: "DELETE" });
}

async function getPerfiles() {
  if (USAR_MOCK) {
    ensureMockStore();
    return [..._mockStore.perfiles];
  }
  const raw = await fetchJson("/api/perfiles");
  return normalizarListaSimple(raw);
}

async function getMenus() {
  if (USAR_MOCK) {
    ensureMockStore();
    return [...(_mockStore.menus || [])];
  }
  const raw = await fetchJson("/api/menus");
  return normalizarListaSimple(raw);
}

async function postPerfil(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const n = { id_perfil: Math.max(..._mockStore.perfiles.map(p => p.id_perfil), 0) + 1, ...body };
    _mockStore.perfiles.push(n);
    return n;
  }
  return fetchJson("/api/perfiles", { method: "POST", body: JSON.stringify(body) });
}

async function deletePerfil(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    _mockStore.perfiles = _mockStore.perfiles.filter(p => String(p.id_perfil) !== String(id));
    return { ok: true };
  }
  return fetchJson("/api/perfiles/" + id, { method: "DELETE" });
}

async function postMenu(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const n = { id_menu: Math.max(...(_mockStore.menus || []).map(m => m.id_menu), 0) + 1, ...body };
    if (!_mockStore.menus) _mockStore.menus = [];
    _mockStore.menus.push(n);
    return n;
  }
  return fetchJson("/api/menus", { method: "POST", body: JSON.stringify(body) });
}

async function deleteMenu(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    _mockStore.menus = (_mockStore.menus || []).filter(m => String(m.id_menu) !== String(id));
    return { ok: true };
  }
  return fetchJson("/api/menus/" + id, { method: "DELETE" });
}

async function postPermiso(body) {
  if (USAR_MOCK) {
    ensureMockStore();
    const n = { id_permiso: Math.max(...(_mockStore.permisos_catalogo || []).map(p => p.id_permiso), 0) + 1, ...body };
    if (!_mockStore.permisos_catalogo) _mockStore.permisos_catalogo = [];
    _mockStore.permisos_catalogo.push(n);
    return n;
  }
  return fetchJson("/api/administrador/permisos/", { method: "POST", body: JSON.stringify(body) });
}

async function deletePermiso(id) {
  if (USAR_MOCK) {
    ensureMockStore();
    _mockStore.permisos_catalogo = (_mockStore.permisos_catalogo || []).filter(p => String(p.id_permiso) !== String(id));
    return { ok: true };
  }
  return fetchJson("/api/administrador/permisos/" + id, { method: "DELETE" });
}

async function postPerfilPermiso(idPerfil, idPermiso) {
  if (USAR_MOCK) {
    ensureMockStore();
    // Simular asociación
    return { ok: true };
  }
  return fetchJson(`/api/perfiles/${idPerfil}/permisos/${idPermiso}`, { method: "POST" });
}

async function getPermisos() {
  if (USAR_MOCK) {
    ensureMockStore();
    return [...(_mockStore.permisos_catalogo?.length ? _mockStore.permisos_catalogo : [])];
  }
  try {
    const raw = await fetchJson("/api/administrador/permisos");
    return normalizarListaSimple(raw);
  } catch (e) {
    return [];
  }
}

/**
 * Lista volantes opcional para combos (derivada del mock).
 */
async function getVolantes(filters = {}) {
  if (USAR_MOCK) {
    ensureMockStore();
    let v = [..._mockStore.volantes];
    if (filters.id_estudiante)
      v = v.filter((x) => String(x.id_estudiante) === String(filters.id_estudiante));
    if (filters.id_periodo)
      v = v.filter((x) => String(x.id_periodo) === String(filters.id_periodo));
    return v;
  }
  const q = new URLSearchParams(filters).toString();
  const raw = await fetchJson(`/api/asistente/volantes${q ? `?${q}` : ""}`);
  return normalizarListaSimple(raw);
}

window.api = {
  USAR_MOCK,
  API_BASE,
  login,
  getEstudiantes,
  getEstudiante,
  postEstudiante,
  putEstudiante,
  deleteEstudiante,
  getProgramas,
  postPrograma,
  putPrograma,
  deletePrograma,
  getCatalogoAsignaturas,
  postAsignaturaCatalog,
  putAsignaturaCatalog,
  deleteAsignaturaCatalog,
  postPlanEstudioSemestre,
  deletePlanEstudioSemestre,
  postPlanEstudioAsignatura,
  deletePlanEstudioAsignatura,
  getPeriodos,
  postPeriodo,
  putPeriodo,
  deletePeriodo,
  getReglasCobro,
  postReglaCobro,
  putReglaCobro,
  deleteReglaCobro,
  getAsignaturas,
  getPlanPorPrograma,
  getPlanPorProgramaMock,
  postVolante,
  postVolantesMasivo,
  postCobroAdicional,
  deleteMovimiento,
  getCuentaCorriente,
  getSaldo,
  postPago,
  getPagos,
  getMovimientosPendientes,
  reporteListadoGeneral,
  reporteIngresoEsperado,
  reportePendientes,
  reporteIngresoReal,
  reporteCartera,
  getUsuarios,
  postUsuario,
  putUsuario,
  deleteUsuario,
  getPerfiles,
  postPerfil,
  deletePerfil,
  getMenus,
  postMenu,
  deleteMenu,
  getPermisos,
  postPermiso,
  deletePermiso,
  postPerfilPermiso,
  getVolantes,
  getCobrosAdicionalesDisponibles() {
    ensureMockStore();
    return [..._mockStore.cobros_adicionales_disponibles];
  },
  getCodigosDetalle,
  postCodigoDetalle,
  putCodigoDetalle,
  deleteCodigoDetalle,
  /** Utilidades para pantallas que reordenan o normalizan en cliente */
  normalizarListaEstudiantes,
  sortPeriodosRecientesPrimero,
};
