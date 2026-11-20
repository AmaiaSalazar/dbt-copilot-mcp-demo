# MCP oficial de dbt con el proyecto local

Este proyecto usa el paquete oficial `dbt-mcp`, instalado desde `requirements-mcp.txt`. El lanzador `demo.py mcp` habilita el conjunto de herramientas CLI y fija `DBT_PROJECT_DIR`, `DBT_PATH`, `DBT_PROFILES_DIR` y `DEMO_ROOT` para este equipo.

No requiere cuenta de dbt Platform. Los métodos de Discovery en la nube y Semantic Layer no forman parte de esta demo. Para lineage local usamos **`get_lineage_dev`** y para detalles **`get_node_details_dev`**, no los métodos de Discovery con nombres parecidos.

## 1. Validar el servidor

Después de build:

```bash
.venv/bin/python scripts/check_mcp.py
```

En Windows usa `.\.venv\Scripts\python.exe`. El script abre una sesión real por stdio, inicializa el protocolo, enumera herramientas y verifica que están disponibles las necesarias para la demo.

## 2. Generar configuración con rutas reales

```bash
.venv/bin/python demo.py mcp-config
```

En Windows ejecuta `.\.venv\Scripts\python.exe demo.py mcp-config`.

El comando imprime JSON con `mcpServers`, el Python absoluto del entorno y la ruta absoluta a `demo.py`. Claude Desktop y Cursor suelen aceptar ese formato. No reemplaces la configuración MCP existente: integra la entrada `dbt-demo` y conserva los demás servidores.

En VS Code, el proyecto ya incluye `.vscode/mcp.json`. Esa configuración usa la ruta de macOS/Linux `${workspaceFolder}/.venv/bin/python`. En Windows cambia `command` a `${workspaceFolder}/.venv/Scripts/python.exe`; conserva `args` como `["${workspaceFolder}/demo.py", "mcp"]`.

Si prefieres usar las rutas absolutas que imprime `mcp-config` en VS Code, adapta la entrada al formato de VS Code: usa el contenedor superior `servers` y añade `"type": "stdio"` al servidor. Copia los valores de `command` y `args` generados; no pegues directamente el contenedor `mcpServers`.

Si el cliente tiene una interfaz de configuración, introduce como comando el valor de `command` y como argumentos los dos valores de `args`. Reinicia o recarga la conexión MCP y comprueba las herramientas disponibles. El lanzador conserva stdout para el protocolo; no requiere activar el entorno en el cliente.

La integración en una aplicación concreta se hace en el equipo del presentador. La configuración debe regenerarse al cambiar de carpeta o de ordenador.

## 3. Prompts preparados

### Comprender el modelo y demostrar el lineage

> Usa las herramientas del MCP dbt-demo. Consulta los detalles locales de mart_sales_by_country y su lineage completo de antecesores con get_lineage_dev y depth=0. Explica en español, en un máximo de 6 frases, qué calcula, su granularidad, qué pedidos excluye y cuáles son sus cuatro capas. Indica las herramientas utilizadas. No modifiques ficheros.

Esperado: una fila por país, EUR, solo completed, dos fuentes y las cuatro capas. En `get_lineage_dev`, `depth=0` significa recorrer el lineage completo. El asistente debe usar `get_node_details_dev` y `get_lineage_dev` con los argumentos expuestos por el servidor.

### Consultar el resultado

> Usa la herramienta show de dbt para ejecutar SELECT country, total_sales, order_count FROM marts.mart_sales_by_country ORDER BY country. Resume los resultados y calcula el total. No uses execute_sql de dbt Platform.

Esperado: DE 100, ES 350, FR 150; total 600 EUR, 7 pedidos.

### Impacto de un cambio (reserva)

> Consulta con el MCP el lineage descendente de stg_orders. Si cambiamos el cálculo de order_amount, ¿qué modelos derivados deben revisarse? Propón una selección dbt para reconstruirlos y validar sus tests. No ejecutes cambios.

Esperado: `int_orders_enriched` y `mart_sales_by_country`, selección `stg_orders+`; revisar también la comprobación de negocio del mart.

## Qué mostrar

Enseña al menos una llamada visible y su respuesta. La IA interpreta la evidencia; el MCP proporciona acceso a herramientas y contexto. La precisión de la explicación se contrasta con los resultados y el SQL.

Un asistente alojado en la nube necesita Internet. Para una sesión completamente offline también hay que disponer de un cliente y modelo de IA locales compatibles con MCP; no se incluye la descarga de un modelo en esta carpeta.

## Referencias oficiales

- https://docs.getdbt.com/docs/dbt-ai/setup-local-mcp
- https://github.com/dbt-labs/dbt-mcp
