from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

class LLMAdapter:
    def query(self, system_prompt, user_prompt, **kwargs):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=kwargs.get("temperature", 0.2),
            max_tokens=kwargs.get("max_tokens", 2000)
        )
        return json.loads(response.choices[0].message.content)