# Social post

How much have we sold by country, and where does that number come from?

I built a small, fully local dbt demo to answer that question end to end: from two CSV files, through tested transformations, to analytical marts in DuckDB. It also shows how GitHub Copilot can use real dbt project metadata through the official dbt-mcp server to explore lineage and help shape a follow-up model.

The sales mart reports **EUR 600 across 7 completed orders**. The project keeps pending and cancelled orders in the reusable intermediate model, then applies the completed-order rule in the mart. The build covers 6 models and 21 tests.

The main takeaway: an AI assistant is more useful when it can work with a project's actual metadata and tools, and its suggestions still need review and tests.

The demo runs locally with DuckDB; no cloud warehouse, Docker, or dbt Platform account is needed.

- Full guide: https://github.com/AmaiaSalazar/dbt-copilot-mcp-demo/blob/main/DEMO_DOCUMENTATION.md
- Source code and sample data: https://github.com/AmaiaSalazar/dbt-copilot-mcp-demo

#dbt #DuckDB #DataEngineering #GitHubCopilot #MCP
