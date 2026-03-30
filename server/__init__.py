"""
server/__init__.py

This package exists to satisfy `openenv validate`, which requires server/app.py
with a main() function.

When uvicorn runs `server:app`, Python resolves `server` as THIS package
(packages take priority over modules). So we load the actual server.py
(sibling file at the parent /app directory) using importlib to avoid circular
imports, and re-export its `app` object.
"""

import importlib.util
import os
import sys

# Load /app/server.py as a module named "_server_module"
_server_py = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server.py")
_spec = importlib.util.spec_from_file_location("_server_module", _server_py)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

# Re-export the FastAPI app so `uvicorn server:app` works
app = _mod.app
