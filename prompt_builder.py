"""
prompt_builder.py
Module 1: Prompt Builder for AI-Powered Insurance Claim Assistant

Bridges the FAISS retrieval layer and the LLM by constructing
structured, hallucination-resistant prompts.
"""

import logging
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


@dataclass
class PromptResult:
    """Holds the assembled prompt and its metadata."""
    prompt: str
    question: str
    context_length: int


class PromptBuilderError(Exception):
    """Raised when prompt assembly fails due to invalid inputs."""


class PromptBuilder:
    """
    Constructs structured prompts for an Insurance Claim Assistant LLM.

    Enforces strict grounding rules to prevent hallucination:
    - The model must answer only from the supplied policy context.
    - The model must respond with a standard message when context is insufficient.

    Compatible with LangChain PromptTemplate pipelines and any
    instruction-tuned LLM (Gemma, Llama, etc.).

    Example:
        >>> builder = PromptBuilder()
        >>> result = builder.build_prompt(
        ...     question="Is flood damage covered?",
        ...     context="Flood damage is covered under Section 4.2..."
        ... )
        >>> print(result.prompt)
    """

    _UNAVAILABLE_RESPONSE = "Information not available in the policy document."

    _SYSTEM_TEMPLATE = """You are an Insurance Claim Assistant.
Your role is to help users understand their insurance policy by answering questions
accurately and professionally based solely on the policy document provided.

RULES:
1. Answer ONLY using the information present in the POLICY CONTEXT below.
2. Do NOT invent, assume, or infer any policy details not explicitly stated.
3. Do NOT reference external knowledge, general insurance norms, or assumptions.
4. If the context does not contain sufficient information to answer, respond with exactly:
   "{unavailable_response}"
5. Be concise, factual, and professional in your response.

---
POLICY CONTEXT:
{context}

---
QUESTION:
{question}

---
ANSWER:"""

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def build_prompt(self, question: str, context: str) -> PromptResult:
        """
        Assemble a grounded LLM prompt from a user question and policy context.

        Args:
            question: The user's natural-language insurance question.
            context:  Relevant policy text retrieved from the vector store.

        Returns:
            PromptResult containing the final prompt string and metadata.

        Raises:
            PromptBuilderError: If question or context are empty/non-string.
        """
        self._validate(question, context)

        prompt = self._SYSTEM_TEMPLATE.format(
            unavailable_response=self._UNAVAILABLE_RESPONSE,
            context=context.strip(),
            question=question.strip(),
        )

        self._logger.info(
            "Prompt built | question_chars=%d | context_chars=%d",
            len(question),
            len(context),
        )

        return PromptResult(
            prompt=prompt,
            question=question.strip(),
            context_length=len(context),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate(self, question: str, context: str) -> None:
        """Raise PromptBuilderError for blank or non-string inputs."""
        for field_name, value in (("question", question), ("context", context)):
            if not isinstance(value, str):
                raise PromptBuilderError(
                    f"'{field_name}' must be a string, got {type(value).__name__}."
                )
            if not value.strip():
                raise PromptBuilderError(f"'{field_name}' must not be empty.")
