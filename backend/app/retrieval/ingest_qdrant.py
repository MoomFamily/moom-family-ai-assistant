import json, sys
from qdrant_client import QdrantClient, models
from app.core.config import settings
from app.providers.gemini import GeminiProvider
def main(path: str):
    provider=GeminiProvider(); client=QdrantClient(url=settings.qdrant_url,api_key=settings.qdrant_api_key or None)
    if not client.collection_exists(settings.qdrant_collection):
        client.create_collection(collection_name=settings.qdrant_collection,vectors_config=models.VectorParams(size=settings.embedding_dimension,distance=models.Distance.COSINE))
    points=[]
    with open(path,encoding='utf-8') as f:
        for i,line in enumerate(f):
            item=json.loads(line); text=item['text']; vector=provider.embed(text)
            points.append(models.PointStruct(id=int(item.get('id',i+1)),vector=vector,payload={'text':text,'source':item.get('source','')}))
    if points: client.upsert(collection_name=settings.qdrant_collection,points=points)
    print(f'Indexed {len(points)} chunks')
if __name__=='__main__': main(sys.argv[1])
