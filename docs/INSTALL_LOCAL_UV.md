# Local Development with uv

This guide explains how to run OpenConstructionERP from a cloned repository using `uv` for Python and `npm` for the frontend.
Use this workflow if you want to develop on top of the codebase, not just install the packaged app from PyPI.

This document intentionally covers only local source setup. It does not cover forks, remotes, or GitHub workflow.

---

## TL;DR

Run these commands from the repository root:

```bash
uv venv --python 3.12
source .venv/bin/activate

nvm use

cd frontend
npm ci --no-audit --no-fund
cd ..

uv pip install -e "./backend[server,dev]"
```

Then start the app in two terminals:

```bash
# Terminal 1
cd backend
source ../.venv/bin/activate
uvicorn app.main:create_app --factory --reload --port 8000
```

```bash
# Terminal 2
nvm use
cd frontend
npm run dev
```

Open:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

---

## 1. Prerequisites

Before you start, make sure these tools are installed:

- Python 3.12+
- Node.js 20.x
- `uv`
- `npm`

This repository includes a `.nvmrc` file with `20`, so if your team uses `nvm` the easiest way to get the correct Node version is:

```bash
nvm use
```

If Node 20 is not installed yet, run:

```bash
nvm install 20
nvm use 20
```

Quick checks:

```bash
python3 --version
node --version
npm --version
uv --version
```

Why these matter:

- Python runs the FastAPI backend.
- Node and npm run the React frontend.
- Node 20 is the recommended frontend runtime for this repository.
- `uv` creates the virtual environment and installs Python packages faster than plain `pip`.

---

## 2. Create a Project Virtual Environment

From the repository root:

```bash
uv venv --python 3.12
source .venv/bin/activate
```

Why:

- `uv venv --python 3.12` creates a repo-local virtual environment in `.venv`.
- `source .venv/bin/activate` makes sure packages install into this project environment, not into your system Python.

On Windows PowerShell, activation is:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Frontend Dependencies

```bash
nvm use
cd frontend
npm ci --no-audit --no-fund
cd ..
```

Why this step matters:

- `npm ci` installs the exact frontend dependency tree from `package-lock.json`.
- the frontend dev server needs these packages before `npm run dev` can run.
- `--no-audit --no-fund` reduces extra network calls and setup noise during local onboarding.

For normal local development, you do not need to build the frontend before the editable backend install.

If you need to build a distributable Python wheel that bundles the pre-built frontend, run:

```bash
nvm use
cd frontend
npm ci --no-audit --no-fund
npm run build
cd ..
```

That extra build step is for packaging, not for everyday editable development.

---

## 4. Install the Backend in Editable Mode

```bash
uv pip install -e "./backend[server,dev]"
```

What this means:

- `uv pip install`: use `uv` to perform a pip-compatible install.
- `-e`: install in editable mode, so your local source files are used directly.
- `./backend`: install the Python package that lives in the `backend` directory.
- `[server,dev]`: also install the optional dependency groups named `server` and `dev`.

Why editable mode matters:

- when you change backend code, you are changing the live code the environment uses.
- you do not need to reinstall the package after every backend edit.

Why the extras matter:

- `server` installs runtime/server dependencies the project expects.
- `dev` installs development tools such as `pytest`, `ruff`, and `mypy`.

---

## 5. Start the Application

Start the backend and frontend in separate terminals.

### Terminal 1: Backend

```bash
cd backend
source ../.venv/bin/activate
uvicorn app.main:create_app --factory --reload --port 8000
```

Why:

- `uvicorn` runs the FastAPI app.
- `--factory` tells Uvicorn that `create_app` returns the application instance.
- `--reload` restarts the backend automatically when Python files change.

### Terminal 2: Frontend

```bash
nvm use
cd frontend
npm run dev
```

Why:

- this starts the Vite development server.
- frontend changes reload automatically in the browser.

Once both are running, open `http://localhost:5173`.

---

## 6. Daily Startup

After the first install, the usual daily workflow is:

```bash
cd OpenConstructionERP
source .venv/bin/activate
```

Then start the two dev servers again:

```bash
# backend terminal
cd backend
source ../.venv/bin/activate
uvicorn app.main:create_app --factory --reload --port 8000
```

```bash
# frontend terminal
nvm use
cd frontend
npm run dev
```

You do not need to rerun `uv pip install -e "./backend[server,dev]"` every day unless dependencies changed.

You do not need to rerun `npm run build` every day. That build is only needed when you want to create a packaged distribution that bundles the frontend assets.

---

## 7. Troubleshooting

### `FileNotFoundError: ... frontend/dist`

Cause: you are building a packaged wheel that bundles the frontend, but the frontend build output has not been generated yet.

Fix:

```bash
nvm use
cd frontend
npm ci --no-audit --no-fund
npm run build
cd ..
```

Then rerun the packaging command.

### `externally-managed-environment`

Cause: packages are being installed into system Python instead of the repo virtual environment.

Fix:

```bash
uv venv --python 3.12
source .venv/bin/activate
```

Then retry the install.

### `uvicorn: command not found`

Cause: the virtual environment is not active, or the backend install did not finish.

Fix:

```bash
source .venv/bin/activate
uv pip install -e "./backend[server,dev]"
```

### `Bus error (core dumped)` when starting Vite

Cause: the frontend toolchain is running under an incompatible Node runtime or stale native packages.

Fix:

```bash
nvm use
cd frontend
rm -rf node_modules
npm ci --no-audit --no-fund
npm run dev
```

If `nvm use` reports that Node 20 is not installed, run `nvm install 20` first.

### Frontend does not open on port 5173

Cause: another process may already be using the port.

Fix: stop the conflicting process or restart `npm run dev` and use the port Vite reports.

---

## 8. Notes

- This workflow is for source development from a cloned repository.
- It is different from `pip install openconstructionerp`, which is meant for packaged app installation.
- We use `uv pip install -e ...` here because we want to edit the codebase directly.
- We do not use `uv sync` at the repo root because this repository is split into a Python backend and a separate Node frontend.
- The repository includes `.nvmrc`, so teammates using `nvm` should run `nvm use` before starting the frontend.
# Local Development with uv

This guide explains how to run OpenConstructionERP from a cloned repository using `uv` for Python and `npm` for the frontend.

Use this workflow if you want to develop on top of the codebase, not just install the packaged app from PyPI.

This document intentionally covers only local source setup. It does not cover forks, remotes, or GitHub workflow.

---

## TL;DR

Run these commands from the repository root:

```bash
uv venv --python 3.12
source .venv/bin/activate

cd frontend
npm install
cd ..

uv pip install -e "./backend[server,dev]"
```

Then start the app in two terminals:

```bash
# Terminal 1
cd backend
source ../.venv/bin/activate
uvicorn app.main:create_app --factory --reload --port 8000
```

```bash
# Terminal 2
cd frontend
npm run dev
```
- Backend API: `http://localhost:8000`

---

## 1. Prerequisites

Before you start, make sure these tools are installed:

- Python 3.12+
 Node.js 20.x
 This repository includes a `.nvmrc` file with `20`, so if your team uses `nvm` the easiest way to get the correct Node version is:

 ```bash
 nvm use
 ```

 If Node 20 is not installed yet, run:

 ```bash
 nvm install 20
 nvm use 20
 ```
- `uv`
- `npm`

node --version
npm --version
uv --version
```

npm ci --no-audit --no-fund

- Python runs the FastAPI backend.
- Node and npm run the React frontend.
- `uv` creates the virtual environment and installs Python packages faster than plain `pip`.

 `--no-audit --no-fund` reduces extra network calls and setup noise during local onboarding
## 2. Create a Project Virtual Environment

From the repository root:

```bash
uv venv --python 3.12
source .venv/bin/activate
nvm use
```

Why:

- `uv venv --python 3.12` creates a repo-local virtual environment in `.venv`.
- `source .venv/bin/activate` makes sure packages install into this project environment, not into your system Python.

On Windows PowerShell, activation is:
nvm use

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

Why this step matters:

- `npm install` downloads the frontend packages.
- the frontend dev server needs these packages before `npm run dev` can run

For normal local development, you do not need to build the frontend before the editable backend install.


```bash
cd frontend
npm install
npm run build
cd ..
```

That extra build step is for packaging, not for everyday editable development.

---

## 4. Install the Backend in Editable Mode

```bash
uv pip install -e "./backend[server,dev]"
```

What this means:

- `uv pip install`: use `uv` to perform a pip-compatible install.
- `-e`: install in editable mode, so your local source files are used directly.
- `./backend`: install the Python package that lives in the `backend` directory.
- `[server,dev]`: also install the optional dependency groups named `server` and `dev`.

Why editable mode matters:

- when you change backend code, you are changing the live code the environment uses
- you do not need to reinstall the package after every backend edit

Why the extras matter:

- `server` installs runtime/server dependencies the project expects
- `dev` installs development tools such as `pytest`, `ruff`, and `mypy`

---

## 5. Start the Application

Start the backend and frontend in separate terminals.

### Terminal 1: Backend

```bash
cd backend
source ../.venv/bin/activate
uvicorn app.main:create_app --factory --reload --port 8000
```

Why:

- `uvicorn` runs the FastAPI app
- `--factory` tells Uvicorn that `create_app` returns the application instance
- `--reload` restarts the backend automatically when Python files change

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Why:

- this starts the Vite development server
- frontend changes reload automatically in the browser

Once both are running, open `http://localhost:5173`.

---

## 6. Daily Startup

After the first install, the usual daily workflow is:

```bash
cd OpenConstructionERP
source .venv/bin/activate
```

Then start the two dev servers again:

```bash
# backend terminal
cd backend
source ../.venv/bin/activate
uvicorn app.main:create_app --factory --reload --port 8000
```

```bash
# frontend terminal
cd frontend
npm run dev
```

You do not need to rerun `uv pip install -e "./backend[server,dev]"` every day unless dependencies changed.

You do not need to rerun `npm run build` every day. That build is only needed when you want to create a packaged distribution that bundles the frontend assets.

---

## 7. Troubleshooting

### `FileNotFoundError: ... frontend/dist`

Cause: you are building a packaged wheel that bundles the frontend, but the frontend build output has not been generated yet.

Fix:

```bash
cd frontend
npm install
npm run build
cd ..
```

Then rerun the packaging command.

### `externally-managed-environment`

Cause: packages are being installed into system Python instead of the repo virtual environment.

Fix:

```bash
uv venv --python 3.12
source .venv/bin/activate
```

Then retry the install.

### `uvicorn: command not found`

Cause: the virtual environment is not active, or the backend install did not finish.

Fix:

```bash
source .venv/bin/activate
uv pip install -e "./backend[server,dev]"
```

### Frontend does not open on port 5173

Cause: another process may already be using the port.

Fix: stop the conflicting process or restart `npm run dev` and use the port Vite reports.

---

## 8. Notes

- This workflow is for source development from a cloned repository.
- It is different from `pip install openconstructionerp`, which is meant for packaged app installation.
- We use `uv pip install -e ...` here because we want to edit the codebase directly.
- We do not use `uv sync` at the repo root because this repository is split into a Python backend and a separate Node frontend.
