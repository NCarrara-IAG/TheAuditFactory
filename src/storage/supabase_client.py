"""Supabase client — structured storage for audits, clients, findings, etc.

Tables expected:
- audits: id, type, client_id, status, created_at, state_json
- clients: id, name, industry, size, contact
- sources: id, audit_id, doc_id, name, type, storage_path
- findings: id, audit_id, agent_id, category, description, severity, sources_json
- risks: id, audit_id, agent_id, title, description, impact, probability
- recommendations: id, audit_id, agent_id, title, effort, impact, timeframe
- scores: id, audit_id, dimension, score, justification
- roi_models: id, audit_id, scenarios_json
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from src.config import settings

logger = logging.getLogger(__name__)


class SupabaseStorage:
    """Wrapper around Supabase client for audit data persistence."""

    def __init__(self):
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self._client = None

    def _get_client(self):
        if self._client is None:
            if not self.url or not self.key:
                logger.warning("Supabase not configured — running in local mode")
                return None
            from supabase import create_client
            self._client = create_client(self.url, self.key)
        return self._client

    def save_audit_state(self, audit_id: str, state: Dict[str, Any]) -> bool:
        client = self._get_client()
        if client is None:
            logger.info(f"[local mode] Would save audit {audit_id}")
            return True
        client.table("audits").upsert({
            "id": audit_id,
            "state_json": state,
        }).execute()
        return True

    def load_audit_state(self, audit_id: str) -> Optional[Dict[str, Any]]:
        client = self._get_client()
        if client is None:
            return None
        result = client.table("audits").select("state_json").eq("id", audit_id).execute()
        if result.data:
            return result.data[0]["state_json"]
        return None

    def upload_file(self, bucket: str, path: str, file_bytes: bytes) -> str:
        client = self._get_client()
        if client is None:
            logger.info(f"[local mode] Would upload to {bucket}/{path}")
            return f"local://{path}"
        client.storage.from_(bucket).upload(path, file_bytes)
        return f"{self.url}/storage/v1/object/public/{bucket}/{path}"
