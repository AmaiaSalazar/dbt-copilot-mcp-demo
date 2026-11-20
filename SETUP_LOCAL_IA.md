# Preparar la demo en local — instrucciones para un asistente de IA

## Objetivo y alcance

Configura esta carpeta en el equipo actual y comprueba que funcionan dbt, DuckDB, los datos ficticios, los tests, la documentación y el servidor MCP oficial. Trabaja dentro de esta carpeta, sin Git y sin servicios de dbt Platform. Conserva los CSV y la lógica de negocio de la demo.

Lee primero `README.md` y sigue estos pasos en orden. Para la configuración del cliente de IA, lee también `MCP.md`.

## 1. Detectar entorno

Identifica sistema operativo, ruta absoluta de esta carpeta y Python disponible. Usa **Python 3.12** para reproducir el entorno probado. Python 3.14 no es compatible con algunas dependencias de esta combinación de dbt.

Si falta Python 3.12:

- macOS con Homebrew: `brew install python@3.12`.
- Windows: instala Python 3.12 desde python.org o `winget install -e --id Python.Python.3.12`; abre una terminal nueva y comprueba `py -3.12 --version`.
- Linux: instala Python 3.12 y su módulo `venv` con el gestor de la distribución; si no está disponible y existe `uv`, usa `uv python install 3.12` y `uv venv --python 3.12 .venv`.

Comprueba que el intérprete elegido informa 3.12 antes de continuar. Si necesitas instalación administrativa sin permisos, comunica el comando pendiente y continúa con las comprobaciones independientes.

## 2. Crear entorno e instalar

Ejecuta desde la carpeta que contiene `dbt_project.yml`.

macOS/Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-mcp.txt
.venv/bin/python -m pip check
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-mcp.txt
.\.venv\Scripts\python.exe -m pip check
```

Si `.venv` procede de otro ordenador o usa otra versión de Python, reemplaza únicamente ese entorno generado y créalo de nuevo. No hace falta activar el entorno ni modificar el perfil global `~/.dbt/profiles.yml`.

DuckDB se instala como dependencia Python: **no necesitas Docker, Node, un servidor SQL ni el ejecutable independiente de DuckDB**. La primera instalación necesita Internet. Las versiones principales están fijadas en los requirements; las dependencias transitivas se resuelven con pip.

Criterio: instalación y `pip check` terminan correctamente.

## 3. Ejecutar y validar

En los ejemplos siguientes, Windows usa `.\.venv\Scripts\python.exe` como intérprete.

```bash
.venv/bin/python demo.py doctor
.venv/bin/python demo.py build
.venv/bin/python demo.py tables
.venv/bin/python demo.py lineage
.venv/bin/python demo.py docs
```

Criterios de aceptación:

- `doctor`: conexión correcta.
- `build`: 6 modelos y 21 tests correctos, sin errores ni skips.
- `tables`: DE=100/2, ES=350/3, FR=150/2; el comando también comprueba esos valores.
- `lineage`: dos fuentes CSV y las cuatro capas hasta el mart.
- existen `demo.duckdb`, `target/manifest.json`, `target/catalog.json` y `target/index.html`.

Los comandos se pueden repetir: las tablas se reconstruyen. Después de mover la carpeta, ejecuta de nuevo build y docs para regenerar rutas y artefactos.

## 4. Abrir documentación y preparar visualización

```bash
.venv/bin/python demo.py serve
```

Abre http://localhost:8080 y comprueba que aparece el modelo final y su grafo. El servidor es un proceso de larga duración: ejecútalo en una terminal independiente. Detén con Ctrl+C. Si el puerto está ocupado, identifica el proceso o usa el comando dbt docs serve con otro puerto y las variables que configura `demo.py`.

Usa `demo.py tables` como visor sin dependencias adicionales. Si el presentador quiere DBeaver, sigue la sección correspondiente de `README.md`; descarga su driver antes de la demo. Cierra su conexión antes de escribir la base con dbt.

## 5. MCP e IA

Sigue `MCP.md`: ejecuta el smoke test, genera la configuración de rutas del equipo actual e intégrala en el cliente que el usuario utilice. Si no sabes cuál utiliza, pregunta solo por ese dato mientras completas el resto de la instalación.

La configuración generada es un fragmento para integrar en la configuración existente, preservando las demás entradas. El esquema exacto depende del cliente. No declares completada la conexión al asistente solo porque arranque el proceso: verifica herramientas visibles y una consulta real desde ese cliente.

Criterio: servidor validado por protocolo y cliente de IA conectado, o bloqueo del cliente identificado explícitamente. La ejecución SQL local funciona sin Internet una vez instaladas las dependencias; una IA remota sí necesita conexión.

## Diagnóstico

| Síntoma | Acción |
|---|---|
| `mashumaro`, `UnserializableField` con Python 3.14 | Recrear `.venv` con Python 3.12. |
| `DEMO_ROOT` no definido al usar dbt directamente | Ejecutar `demo.py`; este fija las variables y el perfil. |
| CSV no encontrado tras mover la carpeta | Reejecutar build y docs mediante `demo.py`. |
| Conflicto de bloqueo DuckDB | Desconectar DBeaver y terminar otras conexiones; ejecutar comandos secuencialmente. |
| Error SSL/proxy al instalar | Usar proxy y CA corporativa del equipo (`HTTPS_PROXY`, `PIP_CERT` cuando proceda); conservar verificación TLS. |
| MCP no encuentra ejecutable | Regenerar configuración con el Python de `.venv` en la nueva ubicación. |
| MCP no ve un modelo nuevo | Regenerar manifest con build o parse y volver a consultar. |

## Entrega

Devuelve al usuario la ruta de la carpeta, versiones instaladas, resultados de cada criterio, comando para arrancar Docs y estado real del MCP en su cliente. Distingue instalación del servidor y conexión del cliente. Usa `DEMO_8_MIN.md` para dejar las pantallas listas para el ensayo.
