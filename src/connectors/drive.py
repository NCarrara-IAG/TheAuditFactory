"""Google Drive connector — stub for document ingestion from Drive."""

from __future__ import annotations

from typing import Any, Dict, List


def list_files_in_folder(folder_id: str) -> List[Dict[str, Any]]:
    """List files in a Google Drive folder. Requires credentials.json + token.json."""
    # TODO: implement with google-api-python-client
    raise NotImplementedError("Google Drive connector not yet implemented")


def download_file(file_id: str, dest_path: str) -> str:
    """Download a file from Google Drive to local path."""
    raise NotImplementedError("Google Drive connector not yet implemented")
