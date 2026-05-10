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
      $("cc-saldo-neto").textContent = COP.format(Math.abs(saldo.saldo_neto));
      $("cc-banner").hidden = false;
      if (saldo.saldo_neto === 0) {
        $("cc-estado-banner").innerHTML =
          '<span class="status-al-dia">Estudiante al día para este período (saldo 0).</span>';
        $("cc-saldo-tile").classList.remove("saldo-highlight");
      } else {
        $("cc-estado-banner").innerHTML =
          '<span class="status-debe">Saldo pendiente: se muestran obligaciones.</span>';
        $("cc-saldo-tile").classList.add("saldo-highlight");
      }

      const movs = Array.isArray(movsAll) ? movsAll : [];
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
    }
  }

  function esc(t) {
    const d = document.createElement("div");
    d.textContent = String(t ?? "");
    return d.innerHTML;
  }

  window.eliminarMovimiento = async function (id) {
    if (!confirm("¿Seguro que desea eliminar este movimiento?")) return;
    try {
      await api.deleteMovimiento(id);
      refrescar();
      if (typeof auth.showToast === "function") {
        auth.showToast("Movimiento eliminado");
      }
    } catch (e) {
      alert(e.message);
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
})();
