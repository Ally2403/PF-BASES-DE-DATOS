(function () {
  const COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  let periodosCache = [];
  var _r1Data = null, _r2Data = null, _r3Data = null, _r4Data = null, _r5Data = null;
  var _r1Meta = {}, _r2Meta = {}, _r3Meta = {}, _r5Meta = {};

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
        "</td><td><span class='badge badge-" + (r.estado || 'PENDIENTE').toLowerCase() + "'>" +
        esc(r.estado || 'PENDIENTE') +
        "</span></td>";
      tb.appendChild(tr);
    });
    _r1Data = rows;
    var _s1 = $("r1-per");
    _r1Meta = { periodo: _s1.value && _s1.selectedIndex >= 0 ? _s1.options[_s1.selectedIndex].text : "Todos los períodos" };
    if ($("btn-r1-pdf")) $("btn-r1-pdf").disabled = !rows.length;
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
    _r2Data = rows;
    var _s2 = $("r2-per");
    _r2Meta = { periodo: _s2.value && _s2.selectedIndex >= 0 ? _s2.options[_s2.selectedIndex].text : "Todos los períodos" };
    if ($("btn-r2-pdf")) $("btn-r2-pdf").disabled = !rows.length;
  }

  async function run3() {
    const prog = $("r3-prog").value;
    if (!prog) {
      auth.showAlert("Debe seleccionar un <strong>programa académico</strong> antes de generar este reporte.", "Programa obligatorio");
      return;
    }
    const per = $("r3-per").value;
    const rows = await api.reportePendientes(prog, per);
    const tb = $("r3-tb");
    tb.innerHTML = "";
    if (!rows.length) {
      const tr = document.createElement("tr");
      const perText = per
        ? (() => { const o = $("r3-per").options[$("r3-per").selectedIndex]; return o && o.value ? " en el período <strong>" + esc(o.textContent) + "</strong>" : ""; })()
        : "";
      tr.innerHTML = "<td colspan='6' style='text-align:center;color:var(--text-muted);padding:1.2rem 0'>" +
        "No hay estudiantes con pagos pendientes" + perText + " para este programa." +
        "</td>";
      tb.appendChild(tr);
      _r3Data = null;
      if ($("btn-r3-pdf")) $("btn-r3-pdf").disabled = true;
      return;
    }
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
    _r3Data = rows;
    var _p3 = $("r3-prog"), _s3 = $("r3-per");
    _r3Meta = {
      programa: _p3.selectedIndex >= 0 ? _p3.options[_p3.selectedIndex].text : "",
      periodo: _s3.value && _s3.selectedIndex >= 0 ? _s3.options[_s3.selectedIndex].text : "Todos los períodos"
    };
    if ($("btn-r3-pdf")) $("btn-r3-pdf").disabled = false;
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
      _r4Data = rows;
      if ($("btn-r4-pdf")) $("btn-r4-pdf").disabled = !rows.length;
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
    _r5Data = rows;
    var _s5 = $("r5-per");
    _r5Meta = { periodo: _s5.value && _s5.selectedIndex >= 0 ? _s5.options[_s5.selectedIndex].text : "Todos los períodos" };
    if ($("btn-r5-pdf")) $("btn-r5-pdf").disabled = !rows.length;
  }

  // ─── PDF export ───────────────────────────────────────────────────────────────────
  function exportPDF(n) {
    var dataMap = { 1: _r1Data, 2: _r2Data, 3: _r3Data, 4: _r4Data, 5: _r5Data };
    var d = dataMap[n];
    if (!d || !d.length) { auth.showToast("No hay datos para exportar.", "error"); return; }
    if (!window.jspdf) { auth.showToast("Librería PDF no cargada.", "error"); return; }
    var jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });
    var pageW = doc.internal.pageSize.getWidth();
    var primary = [26, 58, 92];
    var accent  = [41, 98, 155];
    var TITLES = {
      1: "Reporte 1 · Listado General por Período",
      2: "Reporte 2 · Ingreso Esperado por Período",
      3: "Reporte 3 · Pendientes de Pago",
      4: "Reporte 4 · Ingreso Real de Caja",
      5: "Reporte 5 · Cartera (Crédito Financiero)"
    };
    // Banda de encabezado
    doc.setFillColor(primary[0], primary[1], primary[2]);
    doc.rect(0, 0, pageW, 24, "F");
    doc.setFont("helvetica", "bold");
    doc.setFontSize(13);
    doc.setTextColor(255, 255, 255);
    doc.text(TITLES[n], 14, 11);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8);
    doc.text("Generado: " + new Date().toLocaleString("es-CO"), 14, 18);
    // Línea de contexto (filtros aplicados)
    var y = 32;
    var meta = "";
    if (n === 1 && _r1Meta.periodo) meta = "Período: " + _r1Meta.periodo;
    if (n === 2 && _r2Meta.periodo) meta = "Período: " + _r2Meta.periodo;
    if (n === 3) {
      var parts = [];
      if (_r3Meta.programa) parts.push("Programa: " + _r3Meta.programa);
      if (_r3Meta.periodo) parts.push("Período: " + _r3Meta.periodo);
      meta = parts.join("   ·   ");
    }
    if (n === 5 && _r5Meta.periodo) meta = "Período: " + _r5Meta.periodo;
    if (meta) {
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(primary[0], primary[1], primary[2]);
      doc.text(meta, 14, y);
      y += 7;
    }
    // Datos de la tabla según reporte
    var head, body, colStyles = {};
    if (n === 1) {
      head = [["Carné", "Estudiante", "Programa", "Modalidad", "Monto volante", "Estado"]];
      body = d.map(function(r) {
        return [r.carnet, (r.nombre_estudiante||"")+" "+(r.apellido_estudiante||""), r.nombre_programa, r.modalidad, COP.format(r.monto_total), r.estado||"PENDIENTE"];
      });
      colStyles = { 4: { halign: "right" } };
    } else if (n === 2) {
      var tot2 = 0;
      body = d.map(function(r) { tot2 += Number(r.total_esperado||0); return [r.nombre_periodo, r.nombre_programa, COP.format(r.total_esperado)]; });
      body.push(["", { content: "TOTAL", styles: { fontStyle: "bold" } }, { content: COP.format(tot2), styles: { fontStyle: "bold", halign: "right" } }]);
      head = [["Período", "Programa", "Total esperado"]];
      colStyles = { 2: { halign: "right" } };
    } else if (n === 3) {
      head = [["Carné", "Estudiante", "Cobrado", "Pagado", "Saldo pendiente", "Estado"]];
      body = d.map(function(r) {
        return [r.carnet, (r.nombre_estudiante||"")+" "+(r.apellido_estudiante||""), COP.format(r.total_cobrado), COP.format(r.total_pagado), COP.format(r.saldo_pendiente), r.estado];
      });
      colStyles = { 2: { halign: "right" }, 3: { halign: "right" }, 4: { halign: "right" } };
    } else if (n === 4) {
      var tot4 = 0;
      body = d.map(function(r) { tot4 += Number(r.total_recaudado||0); return [r.nombre_periodo, COP.format(r.total_recaudado)]; });
      body.push([{ content: "TOTAL", styles: { fontStyle: "bold" } }, { content: COP.format(tot4), styles: { fontStyle: "bold", halign: "right" } }]);
      head = [["Período", "Total recaudado"]];
      colStyles = { 1: { halign: "right" } };
    } else if (n === 5) {
      var tot5 = 0;
      body = d.map(function(r) { tot5 += Number(r.valor_credito||0); return [r.carnet, (r.nombre_estudiante||"")+" "+(r.apellido_estudiante||""), r.nombre_programa, COP.format(r.valor_credito)]; });
      body.push(["", "", { content: "TOTAL CARTERA", styles: { fontStyle: "bold" } }, { content: COP.format(tot5), styles: { fontStyle: "bold", halign: "right" } }]);
      head = [["Carné", "Estudiante", "Programa", "Valor crédito"]];
      colStyles = { 3: { halign: "right" } };
    }
    doc.autoTable({
      startY: y,
      head: head,
      body: body,
      theme: "striped",
      headStyles: { fillColor: accent, textColor: [255, 255, 255], fontStyle: "bold", fontSize: 8.5 },
      styles: { fontSize: 8, cellPadding: 2.5 },
      columnStyles: colStyles
    });
    // Pie de página con numeración
    var totalPages = doc.internal.getNumberOfPages();
    for (var i = 1; i <= totalPages; i++) {
      doc.setPage(i);
      doc.setFontSize(7.5);
      doc.setFont("helvetica", "normal");
      doc.setTextColor(120, 120, 120);
      doc.text("Sistema de Gestión Académica · Reportes", pageW / 2, 289, { align: "center" });
      doc.text("Página " + i + " de " + totalPages, pageW / 2, 293, { align: "center" });
    }
    var PREFIXES = { 1: "listado-general", 2: "ingreso-esperado", 3: "pendientes-pago", 4: "ingreso-real", 5: "cartera" };
    var sfx = (meta || "").replace(/[^a-zA-Z0-9]/g, "_").replace(/_+/g, "_").replace(/^_+|_+$/g, "");
    doc.save("reporte-" + PREFIXES[n] + (sfx ? "_" + sfx : "") + ".pdf");
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
    $("btn-r1-pdf").addEventListener("click", function() { exportPDF(1); });
    $("btn-r2-pdf").addEventListener("click", function() { exportPDF(2); });
    $("btn-r3-pdf").addEventListener("click", function() { exportPDF(3); });
    $("btn-r4-pdf").addEventListener("click", function() { exportPDF(4); });
    $("btn-r5-pdf").addEventListener("click", function() { exportPDF(5); });

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
