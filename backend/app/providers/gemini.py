from google import genai
from app.core.config import settings
class GeminiProvider:
    def __init__(self):
        if not settings.gemini_api_key: raise RuntimeError('GEMINI_API_KEY is required')
        self.client=genai.Client(api_key=settings.gemini_api_key)
    def generate(self, prompt: str) -> str:
        response=self.client.models.generate_content(model=settings.gemini_model, contents=prompt)
        return response.text or 'I could not generate a response.'
    def embed(self, text: str) -> list[float]:
        result=self.client.models.embed_content(model=settings.embedding_model, contents=text, config={'output_dimensionality': settings.embedding_dimension})
        return list(result.embeddings[0].values)
