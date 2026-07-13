import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing from .env")
        
        # Initialize the Groq client
        self.client = Groq(api_key=self.api_key)
        # Using Llama-3 70B for top-tier enterprise reasoning
        self.model_name = "llama-3.3-70b-versatile"

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        """Forces the Groq model to output strictly formatted JSON for our data pipeline."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                # Groq natively enforces JSON structure at the API level
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content)
            
        except json.JSONDecodeError:
            raise Exception("Failed to parse Groq JSON output.")
        except Exception as e:
            raise Exception(f"Groq API Error: {e}")