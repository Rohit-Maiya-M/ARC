import os
from dotenv import load_dotenv
import google.genai as genai
from tenacity import retry, wait_exponential, stop_after_attempt

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No GEMINI_API_KEY found in .env")

client = genai.Client(api_key=api_key)


class GeminiService:
    @retry(wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))
    def generate(self, prompt: str, n_predict: int = 512) ->str:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "max_output_tokens": n_predict
            }
        )

        return response.text.strip()