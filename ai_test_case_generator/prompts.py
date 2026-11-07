"""Prompt engineering for test case generation."""

from __future__ import annotations

from .models import GeneratorConfig, TemplateFormat


def build_system_prompt(config: GeneratorConfig) -> str:
    """Build the system prompt for the LLM."""
    test_types_str = ", ".join(t.value for t in config.test_types)
    bdd_instruction = ""
    if config.include_bdd or config.template_format == TemplateFormat.BDD:
        bdd_instruction = """
For each test case, also include a "bdd" object with:
- "given": list of precondition strings (Given ...)
- "when": list of action strings (When ...)
- "then": list of expected outcome strings (Then ...)"""

    return f"""You are an expert QA engineer with 15+ years of experience in software testing.
Your task is to generate comprehensive, well-structured test cases from requirements.

RULES:
- Generate up to {config.max_test_cases} test cases
- Cover these test types: {test_types_str}
- Each test case must be actionable and specific
- Include concrete test data where applicable
- Prioritize test cases by risk and impact
- Think about boundary values, equivalence partitioning, and error guessing

RESPONSE FORMAT — return a single JSON object:
{{
  "title": "Test Suite Title",
  "test_cases": [
    {{
      "id": "TC-001",
      "title": "Short descriptive title",
      "description": "What this test validates",
      "test_type": "functional|edge_case|negative|security|performance|usability|integration|regression",
      "priority": "critical|high|medium|low",
      "preconditions": ["precondition 1", "..."],
      "steps": [
        {{
          "action": "What to do",
          "expected_result": "What should happen",
          "test_data": "Specific data to use (optional)"
        }}
      ],{bdd_instruction}
      "tags": ["tag1", "tag2"],
      "estimated_duration": "2 min"
    }}
  ]
}}

Return ONLY valid JSON. No markdown fences."""


def build_user_prompt(requirement: str, config: GeneratorConfig) -> str:
    """Build the user prompt with the requirement."""
    format_note = ""
    if config.template_format == TemplateFormat.BDD:
        format_note = "\nIMPORTANT: Include BDD scenarios (Given/When/Then) for every test case."

    return f"""Generate test cases for the following requirement:

---
{requirement}
---
{format_note}
Provide thorough coverage including happy paths, edge cases, error handling, and boundary conditions."""
