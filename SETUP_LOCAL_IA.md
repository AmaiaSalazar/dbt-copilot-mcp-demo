# Set Up the Local Demo — Instructions for an AI Assistant

## Goal and scope

Set up this folder on the current computer and verify that dbt, DuckDB, the fictional data, tests, documentation, and the official MCP server work. Work inside this folder without requiring Git or dbt Platform services. Preserve the CSV files and the demo's business logic.

Read `README.md` first and follow these steps in order. For AI client configuration, also read `MCP.md`.

## 1. Check the environment

Identify the operating system, this folder's absolute path, and the available Python versions. Use **Python 3.12** to reproduce the tested environment. Python 3.14 is incompatible with some dependencies in this dbt combination.

If Python 3.12 is missing:

- macOS with Homebrew: `brew install python@3.12`.
- Windows: install Python 3.12 from python.org or run `winget install -e --id Python.Python.3.12`; open a new terminal and check `py -3.12 --version`.
- Linux: install Python 3.12 and its `venv` module using the distribution's package manager. If unavailable and `uv` is installed, run `uv python install 3.12` and `uv venv --python 3.12 .venv`.

Verify that the selected interpreter reports version 3.12 before continuing. If installation requires administrative privileges that are unavailable, tell the user which command is pending and continue with independent checks.

## 2. Create the environment and install dependencies

Run these commands from the folder containing `dbt_project.yml`.

macOS/Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-mcp.txt
.venv/bin/python -m pip check
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-mcp.txt
.\.venv\Scripts\python.exe -m pip check
```

If `.venv` came from another computer or uses a different Python version, replace only that generated environment and recreate it. There is no need to activate the environment or modify the global profile at `~/.dbt/profiles.yml`.

DuckDB is installed as a Python dependency: **Docker, Node, a SQL server, and the standalone DuckDB executable are not required**. The initial installation requires internet access. The main package versions are pinned in the requirements files; pip resolves transitive dependencies.

Acceptance criterion: installation and `pip check` complete successfully.

## 3. Run and validate

In the examples below, Windows uses `.\.venv\Scripts\python.exe` as the interpreter.

```bash
.venv/bin/python demo.py doctor
.venv/bin/python demo.py build
.venv/bin/python demo.py tables
.venv/bin/python demo.py lineage
.venv/bin/python demo.py docs
```

Acceptance criteria:

- `doctor`: connection succeeds.
- `build`: all 6 models and 21 tests pass, with no errors or skips.
- `tables`: DE=100/2, ES=350/3, FR=150/2; the command also checks these values.
- `lineage`: two CSV sources and all four layers through the mart.
- `demo.duckdb`, `target/manifest.json`, `target/catalog.json`, and `target/index.html` exist.

The commands can be repeated; the tables are rebuilt. After moving the folder, run build and docs again to regenerate paths and artifacts.

## 4. Open the documentation and prepare the visualization

```bash
.venv/bin/python demo.py serve
```

Open http://localhost:8080 and verify that the final model and its graph appear. The server is a long-running process, so run it in a separate terminal. Stop it with Ctrl+C. If the port is occupied, identify the process or use `dbt docs serve` with another port and the variables configured by `demo.py`.

Use `demo.py tables` as a viewer with no additional dependencies. If the presenter wants to use DBeaver, follow the relevant section in `README.md` and download its driver before the demo. Close its connection before writing to the database with dbt.

## 5. MCP and AI

Follow `MCP.md`: run the smoke test, generate configuration for the current machine, and integrate it with the client's existing configuration. If you do not know which client the user uses, ask only for that information while completing the rest of the setup.

The generated configuration is a fragment to integrate into the existing configuration while preserving its other entries. The exact format depends on the client. Do not consider the assistant connection complete just because the process starts; verify that the tools are visible and run a real query from that client.

Acceptance criterion: the server passes protocol validation and the AI client is connected, or the client-specific blocker is clearly identified. Local SQL execution works offline after dependencies are installed; a remote AI assistant still needs an internet connection.

## Troubleshooting

| Symptom | Action |
|---|---|
| `mashumaro`, `UnserializableField` with Python 3.14 | Recreate `.venv` with Python 3.12. |
| `DEMO_ROOT` is not set when running dbt directly | Run `demo.py`; it sets the variables and profile. |
| CSV not found after moving the folder | Rerun build and docs through `demo.py`. |
| DuckDB lock conflict | Disconnect DBeaver and close other connections; run commands sequentially. |
| SSL/proxy error during installation | Use the computer's proxy and corporate CA (`HTTPS_PROXY`, `PIP_CERT` when appropriate); keep TLS verification enabled. |
| MCP cannot find the executable | Regenerate the configuration using `.venv`'s Python at the new location. |
| MCP does not see a new model | Regenerate the manifest with build or parse, then query again. |

## Handoff

Tell the user the folder path, installed versions, results for each criterion, the command to start Docs, and the actual MCP status in their client. Distinguish server installation from client connection. The optional local presentation script is `other/DEMO_8_MIN.md`; it is not included in the GitHub repository.
