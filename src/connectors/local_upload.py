"""Local file upload connector — ingest documents from local filesystem."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def ingest_local_files(file_paths: List[str]) -> Dict[str, Any]:
    """Read local files and build a sources index.

    Returns a dict mapping doc_id to metadata:
    {doc_id: {name, path, size_bytes, hash, type}}
    """
    sources_index: Dict[str, Any] = {}

    for fp in file_paths:
        path = Path(fp)
        if not path.exists():
            logger.warning(f"File not found: {fp}")
            continue

        content = path.read_bytes()
        doc_hash = hashlib.sha256(content).hexdigest()[:16]
        doc_id = f"{path.stem}_{doc_hash}"

        sources_index[doc_id] = {
            "name": path.name,
            "path": str(path),
            "size_bytes": len(content),
            "hash": doc_hash,
            "type": path.suffix.lstrip("."),
        }
        logger.info(f"Ingested: {path.name} -> {doc_id}")

    return sources_index


def compute_input_hash(client_context: Dict[str, Any], file_paths: List[str]) -> str:
    """Compute a deterministic hash of all inputs for idempotency."""
    import json
    payload = json.dumps(client_context, sort_keys=True) + "|".join(sorted(file_paths))
    return hashlib.sha256(payload.encode()).hexdigest()
