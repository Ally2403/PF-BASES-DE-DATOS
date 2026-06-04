(function () {
  const COP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

  function $(id) {
    return document.getElementById(id);
  }

  let estudiantesLista = [];
  let _pdfData = null;

  function getFiltradosEstudiantes() {
    const inp = $("cc-filtro-est");
    const q = inp && inp.value ? inp.value.trim().toLowerCase() : "";
    const base = Array.isArray(estudiantesLista) ? estudiantesLista : [];
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

  function renderTablaEstudiantes() {
    const tb = $("cc-tbl-est");
    const lbl = $("cc-lbl-est");
    if (!tb) return;

    const list = getFiltradosEstudiantes();
    tb.innerHTML = "";
    const currentSel = Number($("cc-est").value);

    if (!list.length) {
      tb.innerHTML = '<tr><td colspan="5" style="color:var(--text-muted)">Sin coincidencias.</td></tr>';
    } else {
      list.forEach(function (e) {
        const id = Number(e.id_estudiante);
        const tr = document.createElement("tr");
        tr.dataset.idEstudiante = String(id);
        if (currentSel && id === currentSel) tr.classList.add("is-selected");
        tr.innerHTML =
          "<td>" +
          esc(e.carnet) +
          "</td><td>" +
          esc(e.nombre) +
          "</td><td>" +
          esc(e.apellido) +
          "</td><td>" +
          esc(e.correo) +
          "</td><td>" +
          esc(e.nombre_programa) +
          "</td>";
        tr.onclick = function () {
          $("cc-est").value = id;
          if (lbl) lbl.textContent = "Seleccionado: " + e.nombre + " " + e.apellido + " (" + e.carnet + ")";
          renderTablaEstudiantes();
          refrescar();
        };
        tb.appendChild(tr);
      });
    }
  }

  async function refrescar() {
    $("cc-msg").hidden = true;
    const idEst = $("cc-est").value;
    const idPer = $("cc-per").value;
    if (!idEst || !idPer) return;
    try {
      const movsAll = await api.getCuentaCorriente({
        estudiante: idEst,
        periodo: idPer,
      });
      const saldo = await api.getSaldo({ estudiante: idEst, periodo: idPer });
      $("cc-total-cobros").textContent = COP.format(saldo.total_cobros);
      $("cc-total-pagos").textContent = COP.format(saldo.total_pagos);
      $("cc-saldo-neto").textContent = COP.format(saldo.saldo_neto);
      $("cc-banner").hidden = false;

      // Calcular ESTADO desde los valores numéricos (no viene de la BD)
      const estadoBadges = {
        PAGADO:    { cls: "status-al-dia",  txt: "PAGADO — Estudiante al día" },
        PARCIAL:   { cls: "status-debe",    txt: "PARCIAL — Pago incompleto" },
        PENDIENTE: { cls: "status-debe",    txt: "PENDIENTE — Sin pagos registrados" },
      };
      let estado;
      if (saldo.saldo_neto <= 0) {
        estado = "PAGADO";
      } else if (saldo.total_pagos > 0) {
        estado = "PARCIAL";
      } else {
        estado = "PENDIENTE";
      }
      const badge = estadoBadges[estado] || { cls: "status-debe", txt: estado };
      $("cc-estado-banner").innerHTML = `<span class="${badge.cls}">${badge.txt}</span>`;
      if (estado === "PAGADO") {
        $("cc-saldo-tile").classList.remove("saldo-highlight");
      } else {
        $("cc-saldo-tile").classList.add("saldo-highlight");
      }

      const movs = Array.isArray(movsAll) ? movsAll : [];
      // Guardar snapshot para exportar PDF
      var _selPer = $("cc-per");
      var _estObj = estudiantesLista.find(function (e) {
        return String(e.id_estudiante) === String(idEst);
      });
      _pdfData = {
        saldo: saldo,
        movs: movs,
        estado: estado,
        nombreEst:     _estObj ? (_estObj.nombre + " " + _estObj.apellido) : "",
        carnetEst:     _estObj ? (_estObj.carnet || "") : "",
        programaEst:   _estObj ? (_estObj.nombre_programa || "") : "",
        nombrePeriodo: _selPer.selectedIndex >= 0 ? _selPer.options[_selPer.selectedIndex].text : "",
      };
      if ($("btn-pdf")) $("btn-pdf").disabled = false;
      const cobros = movs.filter(function (m) {
        return m.grupo === "COBRO";
      });
      const pagos = movs.filter(function (m) {
        return m.grupo === "PAGO";
      });
      const tb = $("cc-tbl");
      tb.innerHTML = "";
      function row(m) {
        const tr = document.createElement("tr");
        tr.innerHTML =
          "<td>" +
          esc(m.fecha) +
          "</td><td><code>" +
          esc(m.codigo_detalle) +
          "</code></td><td>" +
          esc(m.descripcion_movimiento) +
          "</td>" +
          "<td class='numeric'>" +
          (m.debito != null ? COP.format(m.debito) : "—") +
          "</td>" +
          "<td class='numeric'>" +
          (m.credito != null ? COP.format(m.credito) : "—") +
          "</td>" +
          "<td class='text-center'>" +
          "<button class='btn btn-small btn-danger' onclick='window.eliminarMovimiento(" + m.id_mov + ")'>Eliminar</button>" +
          "</td>";
        tb.appendChild(tr);
      }
      cobros.forEach(row);
      pagos.forEach(row);
    } catch (e) {
      $("cc-banner").hidden = true;
      $("cc-msg").textContent = e.message;
      $("cc-msg").hidden = false;
      $("cc-msg").className = "alert alert-error";
      _pdfData = null;
      if ($("btn-pdf")) $("btn-pdf").disabled = true;
    }
  }

  function esc(t) {
    const d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  window.eliminarMovimiento = async function (id) {
    if (!await auth.showConfirm("¿Desea eliminar este movimiento? Esta acción no se puede deshacer.")) return;
    if (!await auth.showConfirmCedula(
      "Está a punto de eliminar un movimiento de la cuenta corriente del estudiante.",
      "Este movimiento afecta directamente el saldo del estudiante. Al eliminarlo, el saldo se recalculará automáticamente. Si es un pago, el estudiante quedará con una deuda pendiente; si es un cobro, se reducirá su deuda. Esta acción no se puede deshacer."
    )) return;
    try {
      await api.deleteMovimiento(id);
      refrescar();
      if (typeof auth.showToast === "function") {
        auth.showToast("Movimiento eliminado");
      }
    } catch (e) {
      if (typeof auth.showToast === "function") auth.showToast(e.message, "error");
    }
  };

  document.addEventListener("DOMContentLoaded", async function () {
    const rawEst = await api.getEstudiantes({});
    estudiantesLista =
      typeof api.normalizarListaEstudiantes === "function"
        ? api.normalizarListaEstudiantes(rawEst)
        : Array.isArray(rawEst)
          ? rawEst
          : [];
    const pers = await api.getPeriodos();
    const periodos = Array.isArray(pers) ? pers : [];
    const sP = $("cc-per");

    renderTablaEstudiantes();

    sP.innerHTML = "";
    var phP = document.createElement("option");
    phP.value = "";
    phP.textContent = "— Elija período —";
    sP.appendChild(phP);
    periodos.forEach(function (p) {
      const o = document.createElement("option");
      o.value = p.id_periodo;
      o.textContent = p.nombre_periodo;
      sP.appendChild(o);
    });

    $("cc-est").value = "";
    sP.value = "";

    $("cc-filtro-est").addEventListener("input", renderTablaEstudiantes);
    sP.addEventListener("change", refrescar);
  });

  window.descargarPDF = function () {
    if (!_pdfData) {
      if (typeof auth !== "undefined" && typeof auth.showToast === "function") {
        auth.showToast("Primero consulte los movimientos de un estudiante.", "error");
      }
      return;
    }
    if (typeof window.jspdf === "undefined") {
      alert("La librería PDF no está disponible. Verifique su conexión a internet.");
      return;
    }
    var d = _pdfData;
    var jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });
    var pageW = doc.internal.pageSize.getWidth();
    var primary = [26, 58, 92];
    var accent  = [37, 99, 168];

    // ── Banda de encabezado
    doc.setFillColor(primary[0], primary[1], primary[2]);
    doc.rect(0, 0, pageW, 26, "F");
    doc.setTextColor(255, 255, 255);
    doc.setFont("helvetica", "bold");
    doc.setFontSize(15);
    doc.text("Estado de Cuenta Corriente", 14, 11);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.5);
    doc.text("Sistema de Gestión Universitaria", 14, 19);
    doc.text(
      new Date().toLocaleDateString("es-CO", { day: "2-digit", month: "long", year: "numeric" }),
      pageW - 14, 19, { align: "right" }
    );

    // ── Bloque de datos del estudiante
    doc.setFillColor(244, 248, 255);
    doc.roundedRect(12, 32, pageW - 24, 22, 2, 2, "F");
    doc.setFontSize(8);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(primary[0], primary[1], primary[2]);
    doc.text("Estudiante",   18, 39);
    doc.text("Carné",        95, 39);
    doc.text("Programa",    125, 39);
    doc.text("Período",     175, 39);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9.5);
    doc.setTextColor(30, 30, 30);
    doc.text(String(d.nombreEst     || "—"),                   18, 47);
    doc.text(String(d.carnetEst     || "—"),                   95, 47);
    doc.text(String(d.programaEst   || "—").substring(0, 24), 125, 47);
    doc.text(String(d.nombrePeriodo || "—"),                  175, 47);

    // ── Resumen financiero
    var estadosLabel = {
      PAGADO:    "PAGADO — Al día",
      PARCIAL:   "PARCIAL — Pago incompleto",
      PENDIENTE: "PENDIENTE — Sin pagos",
    };
    doc.autoTable({
      startY: 60,
      head: [["Resumen", ""]],
      body: [
        ["Total Cobros (Débito)",  COP.format(d.saldo.total_cobros)],
        ["Total Pagos (Crédito)",  COP.format(d.saldo.total_pagos)],
        ["Saldo Pendiente",        COP.format(Math.max(0, d.saldo.saldo_neto))],
        ["Estado",                 estadosLabel[d.estado] || d.estado],
      ],
      theme: "grid",
      headStyles: { fillColor: primary, textColor: [255, 255, 255], fontStyle: "bold", fontSize: 8.5 },
      styles: { fontSize: 9, cellPadding: 3 },
      columnStyles: {
        0: { fontStyle: "bold", cellWidth: 65 },
        1: { halign: "right" },
      },
      margin: { left: 12, right: 12 },
      tableWidth: 100,
    });

    // ── Detalle de movimientos
    var cobros  = d.movs.filter(function (m) { return m.grupo === "COBRO"; });
    var pagos   = d.movs.filter(function (m) { return m.grupo === "PAGO";  });
    var allMovs = cobros.concat(pagos);
    var movsBody = allMovs.map(function (m) {
      return [
        String(m.fecha || ""),
        String(m.codigo_detalle || ""),
        String(m.descripcion_movimiento || ""),
        m.debito  != null ? COP.format(m.debito)  : "—",
        m.credito != null ? COP.format(m.credito) : "—",
      ];
    });

    var nextY = doc.lastAutoTable.finalY + 9;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10.5);
    doc.setTextColor(primary[0], primary[1], primary[2]);
    doc.text("Detalle de Movimientos", 14, nextY);

    doc.autoTable({
      startY: nextY + 4,
      head: [["Fecha", "Código", "Descripción", "Cobro", "Pago"]],
      body: movsBody.length ? movsBody : [["" , "", "Sin movimientos registrados.", "", ""]],
      theme: "striped",
      headStyles: { fillColor: accent, textColor: [255, 255, 255], fontStyle: "bold", fontSize: 8.5 },
      styles: { fontSize: 8, cellPadding: 2.5 },
      columnStyles: {
        0: { cellWidth: 22 },
        1: { cellWidth: 24 },
        2: { cellWidth: "auto" },
        3: { halign: "right", cellWidth: 30 },
        4: { halign: "right", cellWidth: 30 },
      },
      alternateRowStyles: { fillColor: [245, 248, 255] },
      margin: { left: 12, right: 12 },
    });

    // ── Pie de página en todas las hojas
    var totalPages = doc.internal.getNumberOfPages();
    for (var i = 1; i <= totalPages; i++) {
      doc.setPage(i);
      doc.setFontSize(7.5);
      doc.setTextColor(160, 160, 160);
      doc.text(
        "Documento generado automáticamente — Sistema de Gestión Universitaria",
        pageW / 2, 289, { align: "center" }
      );
      doc.text("Página " + i + " de " + totalPages, pageW / 2, 293, { align: "center" });
    }

    var filename = "cuenta-corriente_"
      + (d.carnetEst || "estudiante").replace(/[^a-zA-Z0-9]/g, "_")
      + "_" + (d.nombrePeriodo || "periodo").replace(/[^a-zA-Z0-9]/g, "_")
      + ".pdf";
    doc.save(filename);
  };
})();
