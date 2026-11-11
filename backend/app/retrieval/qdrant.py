from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest
from app.core.config import settings
class QdrantRetriever:
    def __init__(self, embed):
        if not settings.qdrant_url: raise RuntimeError('QDRANT_URL is required')
        self.client=QdrantClient(url=settings.qdrant_url,api_key=settings.qdrant_api_key or None)
        self.embed=embed
    def search(self, query: str) -> list[str]:
        result=self.client.query_points(collection_name=settings.qdrant_collection,query=self.embed(query),limit=5,with_payload=True)
        return [str(p.payload.get('text','')) for p in result.points if p.payload]
