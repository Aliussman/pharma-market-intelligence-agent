"""LLM client for interacting with language models"""
import os
from typing import Optional


class LLMClient:
    """Client for LLM operations"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize LLM client
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model name to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
    
    def run(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Run LLM with given prompt
        
        Args:
            prompt: The prompt to send to LLM
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            LLM response text
        """
        try:
            from langchain.llms import OpenAI
            
            llm = OpenAI(
                api_key=self.api_key,
                model_name=self.model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            response = llm(prompt)
            return response
            
        except ImportError:
            raise ImportError("langchain package required. Install with: pip install langchain openai")
        except Exception as e:
            raise RuntimeError(f"LLM request failed: {str(e)}")
