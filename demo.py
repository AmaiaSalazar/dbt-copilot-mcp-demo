"""Punto de entrada portable: usar el Python del entorno .venv."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, DEMO_ROOT=ROOT.as_posix(), DBT_PROFILES_DIR=str(ROOT),
           DBT_SEND_ANONYMOUS_USAGE_STATS="false")
BIN = Path(sys.executable).parent
DBT = BIN / ("dbt.exe" if os.name == "nt" else "dbt")


def dbt(*args):
    subprocess.run([str(DBT), *args], cwd=ROOT, env=ENV, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["doctor", "build", "docs", "serve", "tables", "lineage", "mcp-config", "mcp"])
    args = parser.parse_args()
    if args.command == "doctor":
        dbt("debug")
    elif args.command == "build":
        dbt("build", "--select", "+mart_sales_by_country")
    elif args.command == "docs":
        dbt("docs", "generate")
    elif args.command == "serve":
        dbt("docs", "serve", "--port", "8080", "--no-browser")
    elif args.command == "tables":
        import duckdb
        with duckdb.connect(str(ROOT / "demo.duckdb"), read_only=True) as conn:
            for table in ["base.base_orders", "staging.stg_customers", "intermediate.int_orders_enriched", "marts.mart_sales_by_country"]:
                print(f"\n=== {table} ===", flush=True)
                conn.sql(f"select * from {table} order by 1").show()
            rows = conn.sql("select country, total_sales, order_count from marts.mart_sales_by_country order by country").fetchall()
            expected = [("DE", 100, 2), ("ES", 350, 3), ("FR", 150, 2)]
            if rows != expected:
                raise SystemExit(f"Resultado inesperado: {rows!r}")
    elif args.command == "lineage":
        manifest = json.loads((ROOT / "target/manifest.json").read_text())
        seen = set()
        def visit(uid, depth=0):
            node = manifest["nodes"].get(uid) or manifest["sources"].get(uid)
            print("  " * depth + uid)
            if uid in seen:
                return
            seen.add(uid)
            if node:
                for parent in node.get("depends_on", {}).get("nodes", []):
                    visit(parent, depth + 1)
        visit("model.dbt_local_demo.mart_sales_by_country")
    elif args.command == "mcp-config":
        config = {"mcpServers": {"dbt-demo": {
            "command": sys.executable,
            "args": [str(ROOT / "demo.py"), "mcp"]}}}
        print(json.dumps(config, indent=2))
    elif args.command == "mcp":
        executable = BIN / ("dbt-mcp.exe" if os.name == "nt" else "dbt-mcp")
        mcp_env = dict(ENV, DBT_PROJECT_DIR=str(ROOT), DBT_PATH=str(DBT),
                       DBT_MCP_ENABLE_DBT_CLI="true")
        # No escribir a stdout: está reservado al protocolo MCP stdio.
        subprocess.run([str(executable)], cwd=ROOT, env=mcp_env, check=True)


if __name__ == "__main__":
    main()
