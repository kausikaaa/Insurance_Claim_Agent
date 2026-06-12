"""
answer_generator.py
Module 3: Answer Generator for AI-Powered Insurance Claim Assistant

Orchestrates the interaction between Prompt Builder (Module 1) and LLM Engine (Module 2).
Provides a unified interface for generating insurance policy answers from questions and context.
"""

import logging
import time
from dataclasses import dataclass
from typing import Optional

from Insurance_Claim_Agent.prompt_builder import PromptBuilder, PromptBuilderError
from Insurance_Claim_Agent.llm_engine import LLMEngine, LLMEngineError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


@dataclass
class AnswerResult:
    """Structured result from answer generation process."""
    question: str
    answer: str
    context_length: int
    success: bool
    generation_time: float


class AnswerGeneratorError(Exception):
    """Raised when answer generation fails."""


class AnswerGenerator:
    """
    Orchestrates Prompt Builder and LLM Engine to generate insurance policy answers.

    Handles the complete flow from question + context to final answer:
    1. Validates inputs
    2. Builds structured prompt (via PromptBuilder)
    3. Generates LLM response (via LLMEngine)
    4. Returns structured result with timing metrics

    Example:
        >>> generator = AnswerGenerator(use_mock_llm=True)
        >>> result = generator.generate_response(
        ...     question="Is flood damage covered?",
        ...     context="Flood damage is covered under Section 4.2..."
        ... )
        >>> print(result.answer)
    """

    def __init__(
        self,
        model_name: str = "gemma:2b",
        temperature: float = 0.3,
        use_mock_llm: bool = True,
    ) -> None:
        """
        Initialize the Answer Generator.

        Args:
            model_name: LLM model identifier (e.g., "gemma:2b", "llama2").
            temperature: Sampling temperature for LLM (0.0-1.0).
            use_mock_llm: If True, uses mock LLM (no Ollama required).

        Raises:
            AnswerGeneratorError: If module initialization fails.
        """
        self._logger = logging.getLogger(self.__class__.__name__)

        try:
            self._prompt_builder = PromptBuilder()
            self._llm_engine = LLMEngine(
                model_name=model_name,
                temperature=temperature,
                use_mock=use_mock_llm,
            )
        except Exception as exc:
            error_msg = f"Failed to initialize Answer Generator: {exc}"
            self._logger.error(error_msg)
            raise AnswerGeneratorError(error_msg) from exc

        self._logger.info(
            "AnswerGenerator initialized | model=%s | temperature=%.2f | mock=%s",
            model_name,
            temperature,
            use_mock_llm,
        )

    def generate_response(self, question: str, context: str) -> AnswerResult:
        """
        Generate an answer to an insurance question using provided policy context.

        Workflow:
        1. Validate question and context
        2. Build structured prompt using PromptBuilder
        3. Generate LLM response using LLMEngine
        4. Return structured result with metrics

        Args:
            question: User's insurance-related question.
            context: Relevant policy text retrieved from vector database.

        Returns:
            AnswerResult containing the answer and generation metadata.

        Raises:
            AnswerGeneratorError: If any step in the generation pipeline fails.
        """
        start_time = time.time()

        try:
            # Step 1: Validate inputs
            self._validate_inputs(question, context)

            self._logger.info(
                "Answer generation started | question_length=%d | context_length=%d",
                len(question),
                len(context),
            )

            # Step 2: Build prompt using PromptBuilder
            prompt_result = self._build_prompt(question, context)

            # Step 3: Generate answer using LLMEngine
            llm_response = self._generate_llm_response(prompt_result.prompt)

            # Step 4: Calculate metrics
            generation_time = time.time() - start_time
            # Ensure minimum time precision
            if generation_time == 0.0:
                generation_time = 0.001

            self._logger.info(
                "Answer generation completed | time=%.3fs | answer_length=%d",
                generation_time,
                llm_response.response_length,
            )

            return AnswerResult(
                question=question.strip(),
                answer=llm_response.response_text,
                context_length=len(context),
                success=True,
                generation_time=generation_time,
            )

        except (PromptBuilderError, LLMEngineError) as exc:
            generation_time = time.time() - start_time
            error_msg = f"Answer generation failed: {exc}"
            self._logger.error(error_msg)
            raise AnswerGeneratorError(error_msg) from exc

        except Exception as exc:
            generation_time = time.time() - start_time
            error_msg = f"Unexpected error during answer generation: {exc}"
            self._logger.error(error_msg)
            raise AnswerGeneratorError(error_msg) from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_inputs(self, question: str, context: str) -> None:
        """Validate question and context inputs."""
        if not isinstance(question, str):
            raise AnswerGeneratorError(
                f"Question must be a string, got {type(question).__name__}."
            )

        if not isinstance(context, str):
            raise AnswerGeneratorError(
                f"Context must be a string, got {type(context).__name__}."
            )

        if not question.strip():
            raise AnswerGeneratorError("Question must not be empty.")

        if not context.strip():
            raise AnswerGeneratorError("Context must not be empty.")

        self._logger.debug("Input validation passed")

    def _build_prompt(self, question: str, context: str):
        """Build structured prompt using PromptBuilder."""
        try:
            prompt_result = self._prompt_builder.build_prompt(
                question=question,
                context=context,
            )
            self._logger.debug("Prompt built successfully")
            return prompt_result

        except PromptBuilderError as exc:
            error_msg = f"Prompt building failed: {exc}"
            self._logger.error(error_msg)
            raise AnswerGeneratorError(error_msg) from exc

    def _generate_llm_response(self, prompt: str):
        """Generate response using LLMEngine."""
        try:
            llm_response = self._llm_engine.generate(prompt)
            self._logger.debug("LLM response generated successfully")
            return llm_response

        except LLMEngineError as exc:
            error_msg = f"LLM generation failed: {exc}"
            self._logger.error(error_msg)
            raise AnswerGeneratorError(error_msg) from exc
