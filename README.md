# Local dbt Demo — 8 Minutes

**Start with [SETUP_LOCAL_IA.md](SETUP_LOCAL_IA.md)** to install the project on another computer. That document is written to be handed directly to an AI assistant.

Business question: **How much have we sold by country, and where does that result come from?**

```text
data/orders.csv ─── raw.orders ─── base_orders ─── stg_orders ───┐
                                                              ├─ int_orders_enriched ─ mart_sales_by_country
data/customers.csv ─ raw.customers ─ base_customers ─ stg_customers ┘
                                    base          staging         intermediate          marts
```

The sources read CSV files directly. The four layers are materialized as tables in `demo.duckdb`. There is no prior loading step or `dbt seed`. All amounts are in EUR; no currency conversion is simulated. The CSV files contain 10 orders and 5 customers.

## Daily commands

After installation, run these commands from this folder:

```bash
.venv/bin/python demo.py build
.venv/bin/python demo.py tables
.venv/bin/python demo.py lineage
.venv/bin/python demo.py docs
.venv/bin/python demo.py serve
```

On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe`.

Open http://localhost:8080 to explore dbt Docs; Ctrl+C stops the server. In the catalog, search for `mart_sales_by_country`, open the graph, and expand its ancestors. The manifest is generated at `target/manifest.json`.

`demo.py` automatically sets the project directory, profile location, and absolute CSV paths. It can be invoked from another folder. Using this entry point avoids setting environment variables manually.

## Expected result

| country | total_sales (EUR) | order_count |
|---|---:|---:|
| DE | 100.00 | 2 |
| ES | 350.00 | 3 |
| FR | 150.00 | 2 |

Total: **EUR 600 across 7 completed orders**. Pending and cancelled orders remain in the intermediate model but are excluded from the mart. Staging converts `COMPLETED` to `completed` and cleans the country codes.

There are 6 models and 21 tests, including a business-result assertion. If you intentionally change the data, update that test when the expected results change.

## View the tables

`demo.py tables` displays four tables and closes the connection automatically. It does not require the DuckDB CLI or DBeaver.

For a visual interface, install DBeaver Community, create a **DuckDB** connection, and select this folder's `demo.duckdb` file. Accept the driver download during setup. Open `queries/demo.sql`; the schemas are named exactly `base`, `staging`, `intermediate`, and `marts`.

Disconnect DBeaver before running dbt or MCP queries that open the database from another process; reconnect when finished. Previously generated documentation can be viewed without keeping a DuckDB connection open.

## Documents

- [DEMO_DOCUMENTATION.md](DEMO_DOCUMENTATION.md): complete guide to understanding and reproducing the demo.
- [SETUP_LOCAL_IA.md](SETUP_LOCAL_IA.md): installation, moving between computers, and troubleshooting.
- [MCP.md](MCP.md): connecting the official server to an assistant and prepared prompts.

## Sharing on GitHub

The repository includes the source files, fictional CSVs, and documentation needed to reproduce the demo. The local presentation scripts in `other/` are not published. `.gitignore` excludes that folder, the virtual environment, dbt-generated artifacts, the local database, and local dbt state. Each person creates their own virtual environment by following [SETUP_LOCAL_IA.md](SETUP_LOCAL_IA.md). The project's MCP configuration uses workspace-relative paths; do not publish credentials or configurations with absolute local paths.
