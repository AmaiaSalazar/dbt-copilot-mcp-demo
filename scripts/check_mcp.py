"""Comprueba el handshake y las herramientas reales del servidor oficial."""
import asyncio
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    root = Path(__file__).resolve().parents[1]
    params = StdioServerParameters(command=sys.executable, args=[str(root / "demo.py"), "mcp"])
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            names = {tool.name for tool in tools}
            print("Herramientas disponibles:", ", ".join(sorted(names)))
            required = {"get_lineage_dev", "get_node_details_dev", "show", "build"}
            if not required.issubset(names):
                raise RuntimeError(f"Faltan herramientas: {required - names}")
            for tool in tools:
                if tool.name in {"get_lineage_dev", "get_node_details_dev"}:
                    print(tool.name, tool.inputSchema)
            for name, arguments in [
                ("get_node_details_dev", {"node_id": "mart_sales_by_country"}),
                ("get_lineage_dev", {"unique_id": "model.dbt_local_demo.mart_sales_by_country", "depth": 0}),
                ("show", {"sql_query": "select country, total_sales, order_count from marts.mart_sales_by_country order by country"}),
            ]:
                result = await session.call_tool(name, arguments)
                if result.isError:
                    raise RuntimeError(f"{name}: {result.content}")
                text = "\n".join(getattr(item, "text", "") for item in result.content)
                expected = "350" if name == "show" else "mart_sales_by_country"
                if expected not in text:
                    raise RuntimeError(f"{name}: respuesta sin el modelo esperado: {text}")
                print(f"{name}: consulta real OK")
            print("Handshake MCP, herramientas, manifest y consulta SQL: OK")


if __name__ == "__main__":
    asyncio.run(main())
