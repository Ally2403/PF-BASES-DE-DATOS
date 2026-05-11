(function () {
  const COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  let periodosCache = [];

  function $(id) {
    return document.getElementById(id);
  }

  function tab(btnId, paneId, allBtns, allPanes) {
    document.getElementById(btnId).addEventListener("click", function () {
      allBtns.forEach(function (id) {
        document.getElementById(id).classList.remove("active");
      });
      allPanes.forEach(function (id) {
        document.getElementById(id).hidden = true;
      });
      document.getElementById(btnId).classList.add("active");
      document.getElementById(paneId).hidden = false;
    });
  }

  async function fillPeriod(selId) {
    const s = $(selId);
    s.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija período —";
    s.appendChild(ph);
    periodosCache.forEach(function (p) {
      const o = document.createElement("option");
      o.value = p.id_periodo;
      o.textContent = p.nombre_periodo;
      s.appendChild(o);
    });
    s.value = "";
  }

  async function fillProgramas(selId) {
    const s = $(selId);
    const list = await api.getProgramas();
    const prog = Array.isArray(list) ? list : [];
    s.innerHTML = "";
    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "— Elija programa —";
    s.appendChild(ph);
    prog.forEach(function (p) {
      const o = document.createElement("option");
      o.value = p.id_programa;
      o.textContent = p.nombre_programa;
      s.appendChild(o);
    });
    s.value = "";
  }

  function esc(t) {
    const d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  async function run1() {
    const per = $("r1-per").value;
    const rows = await api.reporteListadoGeneral(per);
    const tb = $("r1-tb");
    tb.innerHTML = "";
    rows.forEach(function (r) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        esc(r.carnet) +
        "</td><td>" +
        esc(r.nombre_estudiante + " " + r.apellido_estudiante) +
        "</td><td>" +
        esc(r.nombre_programa) +
        "</td><td>" +
        esc(r.modalidad) +
        "</td><td class='numeric'>" +
        COP.format(r.monto_total) +
        "</td><td><span class='badge badge-" +
        String(r.estado).toLowerCase() +
        "'>" +
        esc(r.estado) +
        "</span></td>";
      tb.appendChild(tr);
    });
  }

  async function run2() {
    const per = $("r2-per").value;
    const rows = await api.reporteIngresoEsperado(per);
    const tb = $("r2-tb");
    tb.innerHTML = "";
    rows.forEach(function (r) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        esc(r.nombre_periodo) +
        "</td><td>" +
        esc(r.nombre_programa) +
        "</td><td class='numeric'>" +
        COP.format(r.total_esperado) +
        "</td>";
      tb.appendChild(tr);
    });
  }

  async function run3() {
    const prog = $("r3-prog").value;
    if (!prog) {
      auth.showToast("Seleccione un programa obligatorio.", "error");
      return;
    }
    const per = $("r3-per").value;
    const rows = await api.reportePendientes(prog, per);
    const tb = $("r3-tb");
    tb.innerHTML = "";
    rows.forEach(function (r) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        esc(r.carnet) +
        "</td><td>" +
        esc(r.nombre_estudiante + " " + r.apellido_estudiante) +
        "</td><td class='numeric'>" +
        COP.format(r.total_cobrado) +
        "</td><td class='numeric'>" +
        COP.format(r.total_pagado) +
        "</td><td class='numeric'>" +
        COP.format(r.saldo_pendiente) +
        "</td><td>" +
        esc(r.estado) +
        "</td>";
      tb.appendChild(tr);
    });
  }

  async function run4() {
    try {
      const rows = await api.reporteIngresoReal();
      const tb = $("r4-tb");
      tb.innerHTML = "";
      rows.forEach(function (r) {
        const tr = document.createElement("tr");
        tr.innerHTML =
          "<td>" + esc(r.nombre_periodo) + "</td>" +
          "<td class='numeric'>" + COP.format(r.total_recaudado) + "</td>";
        tb.appendChild(tr);
      });
    } catch (e) {
      console.error(e);
      auth.showToast("Error al generar reporte de ingresos.", "error");
    }
  }

  async function run5() {
    const per = $("r5-per").value;
    const rows = await api.reporteCartera(per);
    let tot = 0;
    rows.forEach(function (r) {
      tot += Number(r.valor_credito || 0);
    });
    $("r5-total").textContent = COP.format(tot);
    const tb = $("r5-tb");
    tb.innerHTML = "";
    rows.forEach(function (r) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        esc(r.carnet) +
        "</td><td>" +
        esc(r.nombre_estudiante + " " + r.apellido_estudiante) +
        "</td><td>" +
        esc(r.nombre_programa) +
        "</td><td class='numeric'>" +
        COP.format(r.valor_credito) +
        "</td>";
      tb.appendChild(tr);
    });
  }

  document.addEventListener("DOMContentLoaded", async function () {
    const rawPer = await api.getPeriodos();
    periodosCache = Array.isArray(rawPer) ? rawPer : [];
    await fillPeriod("r1-per");
    await fillPeriod("r2-per");
    await fillPeriod("r3-per");
    await fillPeriod("r5-per");
    await fillProgramas("r3-prog");

    const btns = ["tb1", "tb2", "tb3", "tb4", "tb5"];
    const panes = ["p1", "p2", "p3", "p4", "p5"];
    tab("tb1", "p1", btns, panes);
    tab("tb2", "p2", btns, panes);
    tab("tb3", "p3", btns, panes);
    tab("tb4", "p4", btns, panes);
    tab("tb5", "p5", btns, panes);

    $("btn-r1").addEventListener("click", run1);
    $("btn-r2").addEventListener("click", run2);
    $("btn-r3").addEventListener("click", run3);
    $("btn-r4").addEventListener("click", run4);
    $("btn-r5").addEventListener("click", run5);

    $("p2").hidden = true;
    $("p3").hidden = true;
    $("p4").hidden = true;
    $("p5").hidden = true;

    $("r3-msg").hidden = false;
    $("tb3").addEventListener("click", function () {
      $("r3-msg").hidden = false;
    });
    if ($("r1-per").value) await run1();
    if ($("r2-per").value) await run2();
    await run4(); // Carga automática ya que no tiene filtro
    if ($("r5-per").value) await run5();
  });
})();
