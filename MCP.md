# Official dbt MCP with the local project

This project uses the official `dbt-mcp` package, installed from `requirements-mcp.txt`. The `demo.py mcp` launcher enables the CLI toolset and sets `DBT_PROJECT_DIR`, `DBT_PATH`, `DBT_PROFILES_DIR`, and `DEMO_ROOT` for this machine.

A dbt Platform account is not required. Cloud Discovery and Semantic Layer methods are not part of this demo. For local lineage, use **`get_lineage_dev`**; for model details, use **`get_node_details_dev`**, not similarly named Discovery methods.

## 1. Validate the server

After building the project, run:

```bash
.venv/bin/python scripts/check_mcp.py
```

On Windows, use `.\.venv\Scripts\python.exe`. The script opens a real stdio session, initializes the protocol, lists the tools, and verifies that the tools required for the demo are available.

## 2. Generate configuration with local paths

```bash
.venv/bin/python demo.py mcp-config
```

On Windows, run `.\.venv\Scripts\python.exe demo.py mcp-config`.

The command prints JSON with `mcpServers`, the environment's absolute Python path, and the absolute path to `demo.py`. Claude Desktop and Cursor usually accept this format. Do not replace your existing MCP configuration: add the `dbt-demo` entry and preserve the other servers.

In VS Code, the project already includes `.vscode/mcp.json`. It uses the macOS/Linux path `${workspaceFolder}/.venv/bin/python`. On Windows, change `command` to `${workspaceFolder}/.venv/Scripts/python.exe`; keep `args` as `["${workspaceFolder}/demo.py", "mcp"]`.

If you prefer to use the absolute paths printed by `mcp-config` in VS Code, adapt the entry to VS Code's format: use the top-level `servers` object and add `"type": "stdio"` to the server. Copy the generated `command` and `args` values; do not paste the `mcpServers` object directly.

If the client has a configuration interface, enter the value of `command` as the command and the two values in `args` as its arguments. Restart or reload the MCP connection and check the available tools. The launcher reserves stdout for the protocol; the client does not need to activate the environment.

Configure the integration on the presenter's machine. Regenerate the configuration after moving the folder or changing computers.

## 3. Prepared prompts

### Understand the model and demonstrate lineage

> Use the dbt-demo MCP tools. Get the local details for mart_sales_by_country and its complete upstream lineage with get_lineage_dev and depth=0. In no more than 6 sentences, explain in Spanish what it calculates, its grain, which orders it excludes, and its four layers. Name the tools used. Do not modify any files.

Expected: one row per country, in EUR, completed orders only, two sources, and all four layers. In `get_lineage_dev`, `depth=0` means traverse the complete lineage. The assistant should use `get_node_details_dev` and `get_lineage_dev` with the arguments exposed by the server.

### Query the result

> Use dbt's show tool to run SELECT country, total_sales, order_count FROM marts.mart_sales_by_country ORDER BY country. Summarize the results and calculate the total. Do not use dbt Platform's execute_sql.

Expected: DE 100, ES 350, FR 150; total EUR 600 across 7 orders.

### Impact of a change (backup prompt)

> Use MCP to inspect the downstream lineage of stg_orders. If we change the calculation of order_amount, which downstream models should be reviewed? Suggest a dbt selection to rebuild them and validate their tests. Do not make any changes.

Expected: `int_orders_enriched` and `mart_sales_by_country`, selected with `stg_orders+`; also review the mart's business assertion.

## What to show

Show at least one visible tool call and its response. The AI interprets the evidence; MCP provides access to tools and context. Check the explanation against the results and SQL.

A cloud-hosted assistant needs an internet connection. For a fully offline session, you also need a local AI client and model that support MCP; this folder does not include a model download.

## Official references

- https://docs.getdbt.com/docs/dbt-ai/setup-local-mcp
- https://github.com/dbt-labs/dbt-mcp
