"""Vector store client — document chunking, embedding, and semantic search.

Supports pgvector (via Supabase) or Pinecone.
Used by agents to RAG over client documents.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from src.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Abstraction over vector storage backends."""

    def __init__(self):
        self.backend = settings.vector_store_type

    def index_document(self, doc_id: str, chunks: List[str], metadata: Dict[str, Any]) -> int:
        """Embed and store document chunks. Returns number of chunks indexed."""
        # TODO: implement with langchain text splitter + embeddings
        logger.info(f"[{self.backend}] Would index {len(chunks)} chunks for {doc_id}")
        return len(chunks)

    def search(self, query: str, top_k: int = 5, filter_doc_ids: List[str] | None = None) -> List[Dict[str, Any]]:
        """Semantic search over indexed documents.

        Returns list of {doc_id, chunk_text, score, metadata}.
        """
        # TODO: implement with langchain vectorstore retriever
        logger.info(f"[{self.backend}] Would search: '{query}' (top_k={top_k})")
        return []

    def delete_by_audit(self, audit_id: str) -> int:
        """Remove all vectors associated with an audit (for re-runs)."""
        logger.info(f"[{self.backend}] Would delete vectors for audit {audit_id}")
        return 0
