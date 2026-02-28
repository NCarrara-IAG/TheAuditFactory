"""SharePoint connector — stub for document ingestion from SharePoint."""

from __future__ import annotations

from typing import Any, Dict, List


def list_files_in_site(site_url: str, library: str) -> List[Dict[str, Any]]:
    """List files in a SharePoint document library."""
    # TODO: implement with Office365-REST-Python-Client
    raise NotImplementedError("SharePoint connector not yet implemented")


def download_file(site_url: str, file_path: str, dest_path: str) -> str:
    """Download a file from SharePoint to local path."""
    raise NotImplementedError("SharePoint connector not yet implemented")
