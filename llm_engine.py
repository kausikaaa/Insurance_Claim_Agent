"""
llm_engine.py
Module 2: LLM Engine for AI-Powered Insurance Claim Assistant

Handles all communication with the Large Language Model via Ollama.
Receives formatted prompts and returns structured responses.
"""

import logging
from dataclasses import dataclass
from typing import Optional

try:
    import ollama
except ImportError:
    ollama = None

import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


@dataclass
class LLMResponse:
    """Structured response from the LLM."""
    response_text: str
    model_name: str
    response_length: int
    success: bool


class LLMEngineError(Exception):
    """Raised when LLM communication or configuration fails."""


class LLMEngine:
    """
    Handles communication with Large Language Models via Ollama.

    Supports Gemma (2B, 7B) and Llama models with configurable model selection.
    Provides health checking, prompt validation, and structured response handling.

    Can run in MOCK mode when Ollama is not available (for testing/development).

    Example:
        >>> engine = LLMEngine(model_name="gemma:2b", use_mock=True)
        >>> response = engine.generate("What is insurance?")
        >>> print(response.response_text)
    """

    def __init__(
        self,
        model_name: str = "gemma:2b",
        temperature: float = 0.3,
        timeout: int = 60,
        use_mock: bool = False,
    ) -> None:
        """
        Initialize the LLM Engine.

        Args:
            model_name: Ollama model identifier (e.g., "gemma:2b", "llama2").
            temperature: Sampling temperature (0.0-1.0). Lower = more deterministic.
            timeout: Maximum seconds to wait for response.
            use_mock: If True, uses mock responses (for testing without Ollama).

        Raises:
            LLMEngineError: If ollama package is not installed and use_mock=False.
        """
        self._use_mock = use_mock
        
        if not use_mock and ollama is None:
            raise LLMEngineError(
                "ollama package not found. Install with: pip install ollama\n"
                "OR set use_mock=True for testing without Ollama."
            )

        self._model_name = model_name
        self._temperature = temperature
        self._timeout = timeout
        self._logger = logging.getLogger(self.__class__.__name__)

        mode = "MOCK MODE" if self._use_mock else "LIVE MODE"
        self._logger.info(
            "LLMEngine initialized [%s] | model=%s | temperature=%.2f | timeout=%ds",
            mode,
            self._model_name,
            self._temperature,
            self._timeout,
        )

    def generate(self, prompt: str) -> LLMResponse:
        """
        Generate a response from the LLM for the given prompt.

        Args:
            prompt: Fully formatted prompt string from Prompt Builder.

        Returns:
            LLMResponse containing the model's answer and metadata.

        Raises:
            LLMEngineError: If prompt is invalid, Ollama is unreachable,
                           model is unavailable, or generation fails.
        """
        self._validate_prompt(prompt)

        self._logger.info(
            "Sending request to LLM | model=%s | prompt_length=%d",
            self._model_name,
            len(prompt),
        )

        try:
            if self._use_mock:
                response_text = self._generate_mock_response(prompt)
            else:
                response = ollama.generate(
                    model=self._model_name,
                    prompt=prompt,
                    options={
                        "temperature": self._temperature,
                        "num_predict": 512,
                    },
                )
                response_text = response.get("response", "").strip()

            if not response_text:
                raise LLMEngineError("Model returned empty response.")

            self._logger.info(
                "Response received | model=%s | response_length=%d",
                self._model_name,
                len(response_text),
            )

            return LLMResponse(
                response_text=response_text,
                model_name=self._model_name,
                response_length=len(response_text),
                success=True,
            )

        except Exception as exc:
            if not self._use_mock and "ollama" in str(type(exc).__module__):
                error_msg = f"Ollama API error: {exc}"
            else:
                error_msg = f"Error during generation: {exc}"
            self._logger.error(error_msg)
            raise LLMEngineError(error_msg) from exc

    def health_check(self) -> bool:
        """
        Verify that Ollama is running and the configured model is available.
        In MOCK mode, always returns True.

        Returns:
            True if Ollama is reachable and the model exists, False otherwise.
        """
        if self._use_mock:
            self._logger.info(
                "Health check passed [MOCK MODE] | model=%s (simulated)",
                self._model_name,
            )
            return True

        try:
            available_models = ollama.list()
            model_names = [m["name"] for m in available_models.get("models", [])]

            if self._model_name in model_names:
                self._logger.info(
                    "Health check passed | model=%s is available", self._model_name
                )
                return True
            else:
                self._logger.warning(
                    "Health check failed | model=%s not found. Available: %s",
                    self._model_name,
                    model_names,
                )
                return False

        except Exception as exc:
            self._logger.error("Health check failed | Ollama unreachable: %s", exc)
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_prompt(self, prompt: str) -> None:
        """Raise LLMEngineError if prompt is invalid."""
        if not isinstance(prompt, str):
            raise LLMEngineError(
                f"Prompt must be a string, got {type(prompt).__name__}."
            )
        if not prompt.strip():
            raise LLMEngineError("Prompt must not be empty.")

    def _generate_mock_response(self, prompt: str) -> str:
        """Generate intelligent mock response based on prompt content."""
        prompt_lower = prompt.lower()
        
        # Extract question from prompt
        question_match = re.search(r"QUESTION:\s*(.+?)(?:---|ANSWER:|$)", prompt, re.DOTALL)
        question = question_match.group(1).strip() if question_match else ""
        question_lower = question.lower()
        
        # Extract context from prompt
        context_match = re.search(r"POLICY CONTEXT:\s*(.+?)(?:---|QUESTION:|$)", prompt, re.DOTALL)
        context = context_match.group(1).strip() if context_match else ""
        context_lower = context.lower()
        
        # Check if context is relevant to question
        if not context or len(context) < 20:
            return "Information not available in the policy document."
        
        # Pattern matching for common insurance questions
        if "flood" in question_lower and "flood" in context_lower:
            if "covered" in context_lower:
                # Extract coverage details
                amount_match = re.search(r"(INR|Rs\.?)\s*([0-9,]+)", context)
                amount = amount_match.group(0) if amount_match else "specified amount"
                days_match = re.search(r"(\d+)\s*days?", context)
                days = days_match.group(1) if days_match else "required timeframe"
                
                return f"Yes, flood damage is covered under Section 4.2 of your policy with a maximum coverage of {amount}. Claims must be filed within {days} days of the incident."
        
        if "surgery" in question_lower or "dental" in question_lower:
            if "dental" not in context_lower and "surgery" not in context_lower:
                return "Information not available in the policy document."
        
        if "claim" in question_lower and "reject" in question_lower:
            if "reject" in context_lower or "denial" in context_lower:
                return "Claims may be rejected for reasons stated in the policy context provided."
        
        if "document" in question_lower and "require" in question_lower:
            if "document" in context_lower:
                return "The required documents are listed in the policy section provided."
        
        # Generic contextual response
        if any(word in context_lower for word in ["cover", "include", "eligible"]):
            return f"Based on the policy document, {context[:150]}..."
        
        # Default fallback
        return "Information not available in the policy document."
