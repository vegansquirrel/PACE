# src/adapters/llm_adapter.py
from openai import OpenAI
import os
import json
import logging

logger = logging.getLogger(__name__)

# class LLMAdapter:
#     def query(self, system_prompt, user_prompt, **kwargs):
#         try:
#             client = OpenAI(
#                 api_key=os.getenv("OPENAI_API_KEY"),
#                 timeout=120  # Add connection timeout
#             )
#             response = client.chat.completions.create(
#                 model="gpt-4-turbo",
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 response_format={"type": "json_object"},
#                 temperature=kwargs.get("temperature", 0.2),
#                 max_tokens=kwargs.get("max_tokens", 2000)
#             )
#             return json.loads(response.choices[0].message.content)
#         except json.JSONDecodeError as e:
#             logger.error(f"JSON parsing failed: {str(e)}")
#             return {"error": "Invalid LLM response format"}
#         except Exception as e:
#             logger.critical(f"API connection failed: {str(e)}")
#             return {"error": "Connection to AI service failed"}
        

class LLMAdapter:
    def query(self, system_prompt, user_prompt, **kwargs):
        try:
            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com/v1",
                timeout=120
            )
            response = client.chat.completions.create(
                model="deepseek-chat",  # Update model name
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=kwargs.get("temperature", 0.2),
                max_tokens=kwargs.get("max_tokens", 2000),
                response_format={"type": "json_object"}  # Verify API support
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Deepseek API Error: {str(e)}")
            return {"error": "API request failed"}
