# Social post

An AI assistant can write a SQL query. Can it explain where the result comes from?

We built a local dbt demo to explore that question end to end. Two CSV sources flow through a tested model DAG into DuckDB marts: staging standardizes source values, an intermediate model enriches orders with customer attributes, and the mart applies the completed-order rule before aggregating by country.

With the official dbt-mcp server, GitHub Copilot can inspect actual project metadata and lineage to help develop a follow-up model. The useful part is grounding its suggestions in the project; review and tests still matter.

The demo runs locally with DuckDB; no cloud warehouse, Docker, or dbt Platform account is needed.

We presented this in the latest Tech in Action session. If you missed it, here are the full documentation and demo:

- Full documentation: https://github.com/AmaiaSalazar/dbt-copilot-mcp-demo/blob/main/DEMO_DOCUMENTATION.md
- Demo source code and sample data: https://github.com/AmaiaSalazar/dbt-copilot-mcp-demo

#dbt #DataEngineering #GitHubCopilot #MCP
