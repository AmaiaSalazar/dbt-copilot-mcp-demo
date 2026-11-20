# Demo local de dbt — 8 minutos

**Empieza por [SETUP_LOCAL_IA.md](SETUP_LOCAL_IA.md)** para instalar el proyecto en otro equipo. Ese documento está escrito para entregárselo directamente a un asistente de IA.

Pregunta de negocio: **¿cuánto hemos vendido por país y de dónde sale ese resultado?**

```text
data/orders.csv ─── raw.orders ─── base_orders ─── stg_orders ───┐
                                                              ├─ int_orders_enriched ─ mart_sales_by_country
data/customers.csv ─ raw.customers ─ base_customers ─ stg_customers ┘
                                    base          staging         intermediate          marts
```

Las fuentes leen CSV directamente. Las cuatro capas se materializan como tablas en `demo.duckdb`. No hay carga previa ni `dbt seed`. Todos los importes son EUR; no se simula conversión de moneda. Los CSV contienen 10 pedidos y 5 clientes.

## Comandos diarios

Desde esta carpeta, después de instalar:

```bash
.venv/bin/python demo.py build
.venv/bin/python demo.py tables
.venv/bin/python demo.py lineage
.venv/bin/python demo.py docs
.venv/bin/python demo.py serve
```

En Windows sustituye `.venv/bin/python` por `.venv\Scripts\python.exe`.

Abre http://localhost:8080 para explorar dbt Docs; Ctrl+C detiene el servidor. En el catálogo busca `mart_sales_by_country`, abre el grafo y expande sus antecesores. El manifest se genera en `target/manifest.json`.

`demo.py` fija automáticamente el directorio del proyecto, la ubicación del perfil y la ruta absoluta de los CSV. Se puede invocar desde otra carpeta. Usar este punto de entrada evita configurar variables a mano.

## Resultado esperado

| country | total_sales (EUR) | order_count |
|---|---:|---:|
| DE | 100.00 | 2 |
| ES | 350.00 | 3 |
| FR | 150.00 | 2 |

Total: **600 EUR y 7 pedidos completados**. Los pendientes y cancelados permanecen en intermediate, pero se excluyen del mart. Staging convierte `COMPLETED` en `completed` y limpia los códigos de país.

Hay 6 modelos y 21 tests, incluida una comprobación de los resultados de negocio. Al modificar intencionadamente los datos, adapta ese test si cambian los resultados esperados.

## Mostrar tablas

`demo.py tables` muestra cuatro tablas y cierra la conexión automáticamente. No requiere instalar el CLI de DuckDB ni DBeaver.

Para una interfaz visual, instala DBeaver Community, crea una conexión **DuckDB** y selecciona el fichero `demo.duckdb` de esta carpeta. Acepta la descarga del driver durante la preparación. Abre `queries/demo.sql`; los esquemas se llaman exactamente `base`, `staging`, `intermediate` y `marts`.

Desconecta DBeaver antes de ejecutar dbt o consultas MCP que abran la base desde otro proceso; vuelve a conectarlo al terminar. La documentación ya generada se puede consultar sin mantener abierta una conexión a DuckDB.

## Documentos

- [DEMO_DOCUMENTATION.md](DEMO_DOCUMENTATION.md): documentación completa en inglés para reproducir y entender la demo.
- [SOCIAL_POST.md](SOCIAL_POST.md): resumen listo para compartir.
- [SETUP_LOCAL_IA.md](SETUP_LOCAL_IA.md): instalación, traslado entre equipos y diagnóstico.
- [MCP.md](MCP.md): conectar el servidor oficial a un asistente y prompts.

## Compartir en GitHub

El repositorio incluye los ficheros fuente, los CSV ficticios y la documentación para reproducir la demo. Los guiones locales de presentación de `other/` no se publican. `.gitignore` excluye esa carpeta, el entorno virtual, los artefactos generados por dbt, la base de datos local y el estado local de dbt. Cada persona crea su propio entorno virtual siguiendo [SETUP_LOCAL_IA.md](SETUP_LOCAL_IA.md). La configuración MCP del proyecto usa rutas relativas al workspace; no publiques credenciales ni configuraciones con rutas locales absolutas.
