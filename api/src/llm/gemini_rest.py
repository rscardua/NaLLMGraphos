from typing import List
import os
import requests
import json
from llm.basellm import BaseLLM
from retry import retry


class GeminiChat(BaseLLM):
    """Wrapper around Google Gemini large language models using REST API."""

    def __init__(
        self,
        gemini_api_key: str,
        model_name: str = "gemini-pro",
        max_tokens: int = 1000,
        temperature: float = 0.0,
    ) -> None:
        self.api_key = gemini_api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def _convert_messages_to_gemini_format(self, messages: list[dict[str, str]]) -> str:
        """Convert OpenAI-style messages (list of dicts) to Gemini prompt format."""
        if not messages:
            return ""
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
            else:
                prompt_parts.append(str(content))
        return "\n".join(prompt_parts)

    @retry(tries=3, delay=1)
    def generate(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        try:
            prompt = self._convert_messages_to_gemini_format(messages)

            url = f"{self.base_url}/{self.model_name}:generateContent"
            headers = {
                "Content-Type": "application/json",
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": self.max_tokens,
                    "temperature": self.temperature,
                }
            }

            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    if "content" in result["candidates"][0]:
                        parts = result["candidates"][0]["content"]["parts"]
                        if parts and "text" in parts[0]:
                            return parts[0]["text"]
                return "No response generated"
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                if response.status_code == 400:
                    return "Error: The provided Gemini API key is invalid or request is malformed"
                elif response.status_code == 429:
                    return f"Error: API quota exceeded - {error_msg}"
                else:
                    return f"Error: {error_msg}"
            
        except Exception as e:
            print(f"Retrying LLM call {e}")
            raise Exception()

    async def generateStreaming(
        self,
        messages: list[dict[str, str]],
        onTokenCallback=None,
    ) -> List[str]:
        # For simplicity, use non-streaming and simulate streaming
        try:
            result_text = self.generate(messages)
            
            if onTokenCallback:
                # Simulate streaming by sending chunks
                words = result_text.split()
                chunks = []
                current_chunk = ""
                
                for word in words:
                    current_chunk += word + " "
                    if len(current_chunk) > 50:  # Send chunk every ~50 characters
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
                
                if current_chunk:  # Add remaining text
                    chunks.append(current_chunk.strip())
                
                result = []
                for chunk in chunks:
                    result.append(chunk)
                    token_data = {
                        "choices": [{
                            "delta": {"content": chunk},
                            "finish_reason": None
                        }]
                    }
                    if hasattr(onTokenCallback, '__call__'):
                        callback_result = onTokenCallback(token_data)
                        if hasattr(callback_result, '__await__'):
                            await callback_result
                
                # Send final token
                final_token = {
                    "choices": [{
                        "delta": {"content": ""},
                        "finish_reason": "stop"
                    }]
                }
                if hasattr(onTokenCallback, '__call__'):
                    callback_result = onTokenCallback(final_token)
                    if hasattr(callback_result, '__await__'):
                        await callback_result
                        
                return result
            else:
                return [result_text]
            
        except Exception as e:
            print(f"Error in streaming generation: {e}")
            return [f"Error: {e}"]

    def num_tokens_from_string(self, string: str) -> int:
        """Estimate token count for Gemini models."""
        # Gemini uses a different tokenization, approximate with word count * 1.3
        words = len(string.split())
        return int(words * 1.3)

    def max_allowed_token_length(self) -> int:
        """Returns the maximum number of tokens the LLM can handle."""
        # Updated limits for Gemini models
        if "gemini-1.5" in self.model_name:
            return 1048576  # Gemini 1.5 Pro supports up to 1M tokens
        elif "gemini-pro" in self.model_name:
            return 32768    # Updated limit for Gemini Pro
        else:
            return 8192     # Conservative default
