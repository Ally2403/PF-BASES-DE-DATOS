/**
 * Capa única de acceso al backend FastAPI (Oracle).
 * Capa de API real (FastAPI + Oracle). Sin código mock.
 */

const API_BASE = "";

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
    let msg = res.statusText || "Error HTTP";
    if (data) {
      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail) && data.detail.length) {
        msg = data.detail.map(function(e) { return e.msg || JSON.stringify(e); }).join("; ");
      } else if (data.error) {
        msg = data.error;
      } else if (data.message) {
        msg = data.message;
      }
    }
    // Conflicto de concurrencia: otro usuario realizó la misma operación al mismo tiempo
    if (res.status === 409) {
      msg = msg || "Otro usuario realizó esta operación al mismo tiempo. Recargue la página y verifique el estado actual.";
    }
    // Detectar error de constraint único de Oracle que llegue desde rutas no controladas
    if (/ORA-00001|unique constraint/i.test(msg)) {
      msg = "Operación duplicada: otro usuario realizó el mismo registro al mismo tiempo. Recargue la página y verifique el estado actual.";
    }
    const err = new Error(msg);
    err.status = res.status;
    err.body = data;
    // Si es un conflicto de concurrencia real (no una regla de negocio), recargar la página
    // automáticamente tras 4 s para que el usuario vea datos actualizados.
    // Los 409 de regla de negocio (dependencias, usuario duplicado, etc.) no contienen
    // estas palabras clave y por tanto NO disparan la recarga.
    if (
      res.status === 409 &&
      (/Otro usuario|Operaci[oó]n duplicada|acceso simult[aá]neo/i.test(msg))
    ) {
      err.isConflict = true;
      setTimeout(function () { window.location.reload(); }, 3000);
    }
    throw err;
  }
  return data;
}

/* ---------- API ---------- */

async function login({ username, contrasena }) {
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
    const raw = await fetchJson(q ? `/api/estudiantes?${q}` : "/api/estudiantes");
  return normalizarListaEstudiantes(raw);
}

async function getEstudiante(id) {
    const raw = await fetchJson(`/api/estudiantes/${id}`);
  return raw && raw.data ? raw.data : raw;
}

async function postEstudiante(body) {
    return fetchJson("/api/estudiantes", { method: "POST", body: JSON.stringify(body) });
}

async function putEstudiante(id, body) {
    return fetchJson(`/api/estudiantes/${id}`, { method: "PUT", body: JSON.stringify(body) });
}

async function deleteEstudiante(id) {
    return fetchJson(`/api/estudiantes/${id}`, { method: "DELETE" });
}

async function getProgramas(params = {}) {
  const qp = new URLSearchParams();
  if (params.id_programa != null && String(params.id_programa).trim() !== "") {
    qp.set("id_programa", String(params.id_programa).trim());
  }
  const q = qp.toString();
    const raw = await fetchJson(q ? `/api/programas?${q}` : "/api/programas");
  let list = normalizarListaSimple(raw);
  if (params.id_programa != null && String(params.id_programa).trim() !== "") {
    const filterId = Number(params.id_programa);
    list = list.filter((p) => Number(p.id_programa) === filterId);
  }
  return list;
}

async function postPrograma(body) {
    return fetchJson("/api/programas", { method: "POST", body: JSON.stringify(body) });
}

async function putPrograma(id, body) {
    return fetchJson(`/api/programas/${id}`, { method: "PUT", body: JSON.stringify(body) });
}

async function deletePrograma(id) {
    return fetchJson(`/api/programas/${id}`, { method: "DELETE" });
}

async function getCatalogoAsignaturas() {
    const raw = await fetchJson("/api/asignaturas");
  return normalizarListaSimple(raw);
}

async function postAsignaturaCatalog(body) {
    return fetchJson("/api/asignaturas", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

async function putAsignaturaCatalog(id, body) {
    return fetchJson(`/api/asignaturas/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deleteAsignaturaCatalog(id) {
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
    return fetchJson(`/api/programas/${pid}/planes`, {
    method: "POST",
    body: JSON.stringify({ semestre: sem }),
  });
}

async function deletePlanEstudioSemestre(id_programa, semestre) {
  const pid = Number(id_programa);
  const sem = Number(semestre);
    throw new Error("Eliminar semestres del plan no está habilitado en este backend.");
}

async function postPlanEstudioAsignatura(id_programa, semestre, id_asignatura) {
  const pid = Number(id_programa);
  const sem = Number(semestre);
  const aid = Number(id_asignatura);
    return fetchJson(`/api/programas/${pid}/planes/${sem}/asignaturas`, {
    method: "POST",
    body: JSON.stringify({ id_asignatura: aid }),
  });
}

async function deletePlanEstudioAsignatura(id_programa, semestre, id_asignatura) {
  const pid = Number(id_programa);
  const sem = Number(semestre);
  const aid = Number(id_asignatura);
    return fetchJson(`/api/programas/${pid}/planes/${sem}/asignaturas/${aid}`, { method: "DELETE" });
}

async function getPeriodos(params = {}) {
    const q = new URLSearchParams(params).toString();
  const raw = await fetchJson(q ? `/api/periodos?${q}` : "/api/periodos");
  let r = normalizarListaPeriodosRaw(raw);
  if (params.id_periodo != null && String(params.id_periodo).trim() !== "") {
    r = r.filter((x) => String(x.id_periodo) === String(params.id_periodo));
  }
  return sortPeriodosRecientesPrimero(r);
}

async function postPeriodo(body) {
    return fetchJson("/api/periodos", { method: "POST", body: JSON.stringify(body) });
}

async function putPeriodo(id, body) {
    return fetchJson(`/api/periodos/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deletePeriodo(id) {
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

async function postReglaCobro(body) {
  const pid = Number(body.id_programa);
  const per = Number(body.id_periodo);
  const mod = String(body.modalidad || "").toUpperCase();
  if (!pid || !per || (mod !== "GLOBAL" && mod !== "CREDITOS")) {
    throw new Error("Programa, período y modalidad (GLOBAL | CREDITOS) son obligatorios.");
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
    const mod = String(modalidad || "").toUpperCase();
  const payload = {};
  if (body.valorglobal != null) payload.valor_global = Number(body.valorglobal);
  if (body.valorcredito != null) payload.valor_credito = Number(body.valorcredito);
  return fetchJson(`/api/programas/${id_programa}/periodos/${id_periodo}/reglas/${encodeURIComponent(mod)}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

async function deleteReglaCobro(id_programa, id_periodo, modalidad) {
    const mod = String(modalidad || "").toUpperCase();
  return fetchJson(`/api/programas/${id_programa}/periodos/${id_periodo}/reglas/${encodeURIComponent(mod)}`, {
    method: "DELETE",
  });
}

async function getCodigosDetalle() {
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
    return fetchJson("/api/codigos", { method: "POST", body: JSON.stringify(body) });
}

async function putCodigoDetalle(codigo, body) {
  const key = String(codigo || "").trim().toUpperCase();
    return fetchJson(`/api/codigos/${encodeURIComponent(key)}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deleteCodigoDetalle(codigo) {
  const key = String(codigo || "").trim().toUpperCase();
    return fetchJson(`/api/codigos/${encodeURIComponent(key)}`, { method: "DELETE" });
}

async function getAsignaturas(params = {}) {
  const sem = Number(params.semestre);
  const prog = Number(params.programa);
    if (!Number.isFinite(sem) || !Number.isFinite(prog)) return [];
  const raw = await fetchJson(`/api/programas/${prog}/planes/${sem}/asignaturas`);
  return normalizarListaSimple(raw);
}

async function getPlanPorPrograma(id_programa) {
  const pid = Number(id_programa);
  if (!Number.isFinite(pid) || pid < 1) return [];

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

async function postVolante(body) {
    const raw = await fetchJson("/api/asistente/volantes/individual", {
    method: "POST",
    body: JSON.stringify(body),
  });
  return raw && raw.data ? raw.data : raw;
}

async function postVolantesMasivo(body) {
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
    return fetchJson("/api/asistente/cobros-adicionales", { method: "POST", body: JSON.stringify(body) });
}

async function deleteMovimiento(id_mov) {
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

async function postPago(body) {
  const volantes = await getVolantes({
    id_estudiante: body.id_estudiante,
    id_periodo: body.id_periodo,
  });
  const vol = Array.isArray(volantes) && volantes.length ? volantes[0] : null;

  if (vol && vol.id_volante) {
    // Ruta normal: pago contra volante de matrícula
    return fetchJson("/api/asistente/pagos", {
      method: "POST",
      body: JSON.stringify({
        id_volante: vol.id_volante,
        medio_pago: body.medio_pago,
        valor: body.valor_pagado,
        referencia: body.referencia || null,
        codigo_detalle: body.codigo_detalle || "MPAG",
      }),
    });
  } else {
    // Sin volante: estudiante con cobros adicionales sin matrícula
    return fetchJson("/api/asistente/pagos", {
      method: "POST",
      body: JSON.stringify({
        id_estudiante: body.id_estudiante,
        id_periodo: body.id_periodo,
        medio_pago: body.medio_pago,
        valor: body.valor_pagado,
        referencia: body.referencia || null,
        codigo_detalle: body.codigo_detalle || "MPAG",
      }),
    });
  }
}

async function getPagos(filtros = {}) {
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
    const raw = await fetchJson(`/api/reportes/ingreso-real`);
  return normalizarListaSimple(raw);
}

async function reporteCartera(periodo) {
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
    const raw = await fetchJson("/api/usuarios");
  return normalizarListaSimple(raw);
}

async function postUsuario(body) {
    return fetchJson("/api/usuarios", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

async function putUsuario(id, body) {
    return fetchJson(`/api/usuarios/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function deleteUsuario(id) {
    return fetchJson(`/api/usuarios/${id}`, { method: "DELETE" });
}

async function enviarCredencialesUsuario(id) {
    return fetchJson(`/api/usuarios/${id}/enviar-credenciales`, { method: "POST" });
}

async function getPerfiles() {
    const raw = await fetchJson("/api/perfiles");
  return normalizarListaSimple(raw);
}

async function getMenus() {
    const raw = await fetchJson("/api/menus");
  return normalizarListaSimple(raw);
}

async function postPerfil(body) {
    return fetchJson("/api/perfiles", { method: "POST", body: JSON.stringify(body) });
}

async function deletePerfil(id) {
    return fetchJson("/api/perfiles/" + id, { method: "DELETE" });
}

async function postMenu(body) {
    return fetchJson("/api/menus", { method: "POST", body: JSON.stringify(body) });
}

async function deleteMenu(id) {
    return fetchJson("/api/menus/" + id, { method: "DELETE" });
}

async function postPermiso(body) {
    return fetchJson("/api/administrador/permisos/", { method: "POST", body: JSON.stringify(body) });
}

async function deletePermiso(id) {
    return fetchJson("/api/administrador/permisos/" + id, { method: "DELETE" });
}

async function postPerfilPermiso(idPerfil, idPermiso) {
    return fetchJson(`/api/perfiles/${idPerfil}/permisos/${idPermiso}`, { method: "POST" });
}

async function deletePerfilPermiso(idPerfil, idPermiso) {
    return fetchJson(`/api/perfiles/${idPerfil}/permisos/${idPermiso}`, { method: "DELETE" });
}

async function getPermisos() {
    try {
    const raw = await fetchJson("/api/permisos");
    return normalizarListaSimple(raw);
  } catch (e) {
    return [];
  }
}

/**
 * Lista volantes opcional para combos (derivada del mock).
 */
async function getVolantes(filters = {}) {
    const q = new URLSearchParams(filters).toString();
  const raw = await fetchJson(`/api/asistente/volantes${q ? `?${q}` : ""}`);
  return normalizarListaSimple(raw);
}

window.api = {
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
  enviarCredencialesUsuario,
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
  deletePerfilPermiso,
  getVolantes,
  async getCobrosAdicionalesDisponibles() {
    const raw = await fetchJson("/api/codigos/disponibles");
    return normalizarListaSimple(raw);
  },
  getCodigosDetalle,
  postCodigoDetalle,
  putCodigoDetalle,
  deleteCodigoDetalle,
  /** Utilidades para pantallas que reordenan o normalizan en cliente */
  normalizarListaEstudiantes,
  sortPeriodosRecientesPrimero,
};
