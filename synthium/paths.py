"""Where Synthium's data lives.

The data folder sits next to the package (``codebase/data``). Set
``SYNTHIUM_DATA`` to point somewhere else, for example a synced copy.
"""
from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_DIR = PACKAGE_DIR.parent


def data_dir() -> Path:
    """The data directory: ``$SYNTHIUM_DATA`` if set, else ``<repo>/data``."""
    env = os.environ.get("SYNTHIUM_DATA")
    return Path(env) if env else REPO_DIR / "data"


def data_path(*parts: str) -> Path:
    """A path inside the data directory."""
    return data_dir().joinpath(*parts)
