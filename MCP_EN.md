# Official dbt MCP with the local project

This project uses the official `dbt-mcp` package, installed from `requirements-mcp.txt`. The `demo.py mcp` launcher enables the CLI toolset and sets `DBT_PROJECT_DIR`, `DBT_PATH`, `DBT_PROFILES_DIR`, and `DEMO_ROOT` for this machine.

A dbt Platform account is not required. Cloud Discovery and Semantic Layer methods are not part of this demo. For local lineage, use **`get_lineage_dev`** and for details use **`get_node_details_dev`**, rather than the similarly named Discovery methods.

## 1. Validate the server

After running build:

```bash
.venv/bin/python scripts/check_mcp.py
```

On Windows, use `.\.venv\Scripts\python.exe`. The script opens a real stdio session, initializes the protocol, lists the available tools, and verifies that the tools required for the demo are available.

## 2. Generate configuration with real paths

```bash
.venv/bin/python demo.py mcp-config
```

On Windows, run `.\.venv\Scripts\python.exe demo.py mcp-config`.

The command prints JSON with `mcpServers`, the absolute path to the Python executable, and the absolute path to `demo.py`. Claude Desktop and Cursor usually accept this format. Do not replace your existing MCP configuration: add the `dbt-demo` entry and preserve the other servers.

In VS Code, the project already includes `.vscode/mcp.json`. This configuration uses the macOS/Linux path `${workspaceFolder}/.venv/bin/python`. On Windows, change `command` to `${workspaceFolder}/.venv/Scripts/python.exe`; keep `args` as `["${workspaceFolder}/demo.py", "mcp"]`.

If you prefer to use the absolute paths printed by `mcp-config` in VS Code, adapt the entry to the VS Code format: use the top-level `servers` container and add `"type": "stdio"` to the server. Copy the generated `command` and `args` values; do not paste the `mcpServers` container directly.

If the client has a configuration interface, enter the value of `command` as the command and the two values in `args` as the arguments. Restart or reload the MCP connection and check the available tools. The launcher keeps stdout reserved for the protocol; you do not need to activate the virtual environment in the client.

The integration into a specific application is done on the presenter's machine. Regenerate the configuration when changing folders or computers.

## 3. Prepared prompts

### Understand the model and demonstrate lineage

> Use the dbt-demo MCP tools. Query the local details for mart_sales_by_country and its complete upstream lineage with get_lineage_dev and depth=0. Explain what it calculates, its grain, which orders it excludes, and what its four layers are. State which tools you used. Do not modify any files.

Expected: one row per country, EUR, completed orders only, two sources, and the four layers. In `get_lineage_dev`, `depth=0` means traversing the complete lineage graph. The assistant should use `get_node_details_dev` and `get_lineage_dev` with the arguments exposed by the server.

### Query the result

> Use the dbt show tool to run SELECT country, total_sales, order_count FROM marts.mart_sales_by_country ORDER BY country. Summarize the results and calculate the total. Do not use dbt Platform's execute_sql.

Expected: DE 100, ES 350, FR 150; total 600 EUR, 7 orders.

### Change impact (backup prompt)

> Query the downstream lineage of stg_orders with MCP. If we change the order_amount calculation, which derived models should be reviewed? Propose a dbt selection to rebuild them and validate their tests. Do not execute any changes.

Expected: `int_orders_enriched` and `mart_sales_by_country`, selection `stg_orders+`; also review the mart's business check.

## What to show

Show at least one visible tool call and its response. The AI interprets the evidence; MCP provides access to tools and context. The accuracy of the explanation is checked against the results and the SQL.

A cloud-hosted assistant needs Internet access. For a completely offline session, you also need a local AI client and model that support MCP; downloading a model is outside the scope of this folder.

## Official references

- https://docs.getdbt.com/docs/dbt-ai/setup-local-mcp
- https://github.com/dbt-labs/dbt-mcp
