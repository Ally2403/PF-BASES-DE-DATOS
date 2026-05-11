# Prompt — Ajustes al DDL, backend e integración con el frontend

---

Hola. Tengo un proyecto universitario de gestión de matrículas llamado **Cuenta Corriente del Estudiante**. El proyecto tiene backend en Python (FastAPI) y frontend ya terminado. Te voy a adjuntar los archivos del proyecto. Necesito que me ayudes con varias tareas en orden. **Trabaja una tarea a la vez y espera mi confirmación antes de pasar a la siguiente.**

---

## Contexto clave — léelo antes de todo

**El backend ya está completamente implementado en FastAPI/Python.** No empieces desde cero. Tu trabajo es modificar y ajustar el código existente según las tareas descritas abajo. El frontend también está terminado en HTML, CSS y JavaScript puro, sin ningún framework.

---

## Archivos adjuntos — léelos todos antes de empezar

1. **`entregable3_ddl_final_final.sql`** — DDL completo de Oracle con todas las tablas, secuencias, índices, triggers y vistas del sistema.
2. **El código del backend** (carpeta `backend/`) — API REST en FastAPI/Python ya implementada.
3. **El código del frontend** (carpeta `frontend/`) — ya terminado y funcionando correctamente. **No toques nada del frontend salvo que una tarea lo requiera explícitamente.**
4. **`docker-compose.yml`** — configuración de contenedores.
5. **`.gitignore`** — archivo de exclusiones de Git.

---

## Contexto importante antes de empezar

- El backend y el frontend están en la misma rama `dev` del repositorio, cada uno en su carpeta (`backend/` y `frontend/`).
- La base de datos es Oracle XE corriendo en Docker (contenedor `oracle-universidad`, puerto `1522` externo / `1521` interno, service name `XEPDB1`, usuario `app_user`).
- El frontend ya consume endpoints del backend. **El objetivo es que el backend se acople al frontend, no al revés.**
- Los perfiles de usuario son: **ADMINISTRADOR**, **SUPERVISOR** y **ASISTENTE**, con permisos fijos definidos en el enunciado.

---

## TAREA 1 — Mover el campo ESTADO de VOLANTE_MATRICULA a CUENTA_CORRIENTE

### Qué hay que cambiar y por qué

Actualmente la columna `ESTADO` (valores: PENDIENTE, PARCIAL, PAGADO) está en la tabla `VOLANTE_MATRICULA`. Sin embargo, el estado debe reflejar la situación financiera del estudiante en general (cobros - pagos = 0), no la del volante individual. Por eso debe vivir en `CUENTA_CORRIENTE`.

### Cambios que debes hacer en el DDL

1. **Quitar** la columna `ESTADO` de la tabla `VOLANTE_MATRICULA` y el constraint `CK_VOL_ESTADO` asociado.
2. **Agregar** la columna `ESTADO VARCHAR2(20) DEFAULT 'PENDIENTE' NOT NULL` a la tabla `CUENTA_CORRIENTE`, con su constraint `CHECK (ESTADO IN ('PENDIENTE', 'PARCIAL', 'PAGADO'))`.
3. **Modificar el trigger `TR_ACTUALIZAR_ESTADO_VOLANTE`** para que en lugar de hacer `UPDATE VOLANTE_MATRICULA SET ESTADO = ...` haga `UPDATE CUENTA_CORRIENTE SET ESTADO = ...` donde `ID_ESTUDIANTE` corresponda al volante procesado.
4. **Revisar y ajustar todas las vistas** que referencien `VOLANTE_MATRICULA.ESTADO` o `vm.ESTADO` para que ahora lean `CUENTA_CORRIENTE.ESTADO` o `cc.ESTADO`.
5. **Ajustar los datos semilla** si algún INSERT hace referencia al campo ESTADO de VOLANTE_MATRICULA.

### Lo que debes entregarme

- El DDL completo actualizado con todos estos cambios aplicados.
- Una explicación breve de cada cosa que cambiaste y por qué.
- Dime cómo volver a ejecutar el DDL en SQL Developer sin errores (ya tengo los DROPs al inicio del script).

**Espera mi confirmación antes de pasar a la Tarea 2.**

---

## TAREA 2 — Ajustar el backend a los cambios del DDL

Una vez el DDL esté actualizado y yo lo haya ejecutado en Oracle, ajusta el backend:

1. **Cualquier endpoint que devuelva o use `ESTADO` de `VOLANTE_MATRICULA`** debe actualizarse para leerlo desde `CUENTA_CORRIENTE`.
2. **Cualquier endpoint que devuelva datos del volante** debe dejar de incluir el campo `ESTADO` en ese objeto, y en cambio incluirlo en los datos de la cuenta corriente del estudiante.
3. **Las vistas ya cambiadas en la Tarea 1** se reflejarán automáticamente en los endpoints que usan `SELECT * FROM VW_...` — verifica que sigan funcionando.
4. **No cambies la estructura general del backend** — solo ajusta lo mínimo necesario para reflejar el cambio de columna.

**Espera mi confirmación antes de pasar a la Tarea 3.**

---

## TAREA 3 — Definir qué hacer con Usuarios, Menús y Permisos en el frontend

El frontend tiene actualmente una sección de administración con las siguientes opciones:
- Gestión de usuarios (crear, editar, eliminar) ✅ — esto sí debe estar
- Gestión de perfiles
- Gestión de menús
- Gestión de permisos

El problema es que los permisos por perfil ya están **definidos y fijos** en el enunciado del proyecto:
- ADMINISTRADOR: todos los permisos
- SUPERVISOR: gestionar programas, asignaturas, estudiantes, reglas, códigos, ver reportes
- ASISTENTE: generar cobros, registrar pagos, ver cuenta corriente, ver reportes

No tiene sentido que desde la interfaz se puedan modificar estos permisos en runtime, ya que son parte de la lógica de negocio del sistema.

### Lo que debes hacer

1. **Gestión de usuarios**: mantener completo — el ADMINISTRADOR puede ver, crear, editar y eliminar usuarios. Los endpoints de usuarios deben seguir funcionando igual.
2. **Gestión de perfiles y permisos**: convertir a **solo lectura**. El ADMINISTRADOR puede *ver* qué perfiles existen y qué permisos tiene cada uno, pero **no puede crearlos, editarlos ni eliminarlos** desde la interfaz. Ajusta los endpoints correspondientes para que solo expongan GET, sin POST/PUT/DELETE para estas entidades.
3. **Gestión de menús**: igual que perfiles — solo lectura. Los menús son configuración fija del sistema.
4. **En el backend**: elimina o desactiva los endpoints de creación/edición/eliminación de `PERFIL`, `PERMISO`, `MENU` y `PERFIL_PERMISO`. Solo deja los GET.

Explícame qué endpoints vas a desactivar antes de hacerlo, y espera mi confirmación.

**Espera mi confirmación antes de pasar a la Tarea 4.**

---

## TAREA 4 — Integrar el backend con el frontend

Una vez las tareas anteriores estén listas y funcionando, integra el backend con el frontend.

### Reglas estrictas

1. **NO modifiques nada del frontend** — ni estructura de carpetas, ni componentes, ni estilos, ni lógica de UI. El frontend está terminado y funciona correctamente.
2. **El backend se acopla al frontend**, no al revés. Si hay un endpoint que el frontend llama de cierta manera, el backend debe responder exactamente como el frontend lo espera.
3. Revisa el frontend para identificar:
   - Qué URLs de endpoints consume (ej: `/api/estudiantes`, `/api/auth/login`)
   - Qué estructura JSON espera en las respuestas
   - Qué campos envía en los requests
4. Ajusta el backend para que sus respuestas coincidan exactamente con lo que el frontend espera.
5. Verifica que el CORS esté configurado correctamente para que el frontend pueda llamar al backend sin errores.

### Lo que debes entregarme

- Lista de todos los endpoints que consume el frontend con la URL exacta y el formato de respuesta esperado.
- Lista de cambios que hiciste en el backend para acomodar esas expectativas.
- Instrucciones para levantar todo junto (backend + Oracle Docker) y probar que funciona.

**Espera mi confirmación antes de pasar a la Tarea 5.**

---

## TAREA 5 — Revisar y corregir el .gitignore

Revisa el archivo `.gitignore` actual y verifica que esté ignorando correctamente todo lo que no debe subirse a GitHub, teniendo en cuenta que el proyecto tiene:

**Backend (Python/FastAPI)**

**Frontend (HTML, CSS y JS puro — sin framework ni Node)**

**Generales**

Ten en cuenta que el frontend es HTML, CSS y JavaScript puro, sin ningún framework ni gestor de paquetes.

---

## Reglas generales para todas las tareas

1. **Una tarea a la vez.** No avances sin mi confirmación.
2. **No toques el frontend** salvo que una tarea lo indique explícitamente.
3. **Explícame brevemente qué vas a hacer antes de escribir código**, para que yo pueda validar o corregirte.
4. **Si algo no está claro, pregúntame** antes de inventarte algo.
5. **Los endpoints siempre responden en JSON** con estructura: `{ "data": ..., "message": "...", "success": true/false }`.

---

Empieza por la **Tarea 1**. Explícame qué cambios vas a hacer en el DDL antes de mostrármelos.
