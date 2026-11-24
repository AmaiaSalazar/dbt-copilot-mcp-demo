# Social post

An AI assistant can write a SQL query. Can it explain where the result comes from?

I built a local dbt demo to explore that question end to end. Two CSV sources flow through a tested model DAG into DuckDB marts: staging standardizes source values, an intermediate model enriches orders with customer attributes, and the mart applies the completed-order rule before aggregating by country.

The project includes 6 models and 21 tests, covering data quality constraints and expected business results. Pending and cancelled orders remain available in the reusable intermediate model; the mart applies the business filter so the rule is explicit and testable.

With the official dbt-mcp server, GitHub Copilot can inspect actual project metadata and lineage to help develop a follow-up model. The useful part is grounding its suggestions in the project; review and tests still matter.

The demo runs locally with DuckDB; no cloud warehouse, Docker, or dbt Platform account is needed.

- Full guide: https://github.com/AmaiaSalazar/dbt-copilot-mcp-demo/blob/main/DEMO_DOCUMENTATION.md
- Source code and sample data: https://github.com/AmaiaSalazar/dbt-copilot-mcp-demo

#dbt #DataEngineering #GitHubCopilot #MCP
