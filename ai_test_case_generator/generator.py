"""OpenAI-powered test case generation engine."""

from __future__ import annotations

import json
import os
from typing import Optional

from openai import OpenAI

from .models import (
    BDDScenario,
    GeneratorConfig,
    Priority,
    TemplateFormat,
    TestCase,
    TestStep,
    TestSuite,
    TestType,
)
from .prompts import build_system_prompt, build_user_prompt


class TestGenerator:
    """Generate test cases from requirements using OpenAI GPT models."""

    def __init__(self, config: Optional[GeneratorConfig] = None):
        self.config = config or GeneratorConfig()
        api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY env var or pass api_key in config."
            )
        self.client = OpenAI(api_key=api_key)

    def generate(self, requirement: str, title: Optional[str] = None) -> TestSuite:
        """Generate test cases from a requirement string."""
        system_prompt = build_system_prompt(self.config)
        user_prompt = build_user_prompt(requirement, self.config)

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)
        test_cases = self._parse_test_cases(data)

        suite = TestSuite(
            title=title or data.get("title", "Generated Test Suite"),
            requirement=requirement[:500],
            test_cases=test_cases,
            model_used=self.config.model,
        )
        return suite

    def _parse_test_cases(self, data: dict) -> list[TestCase]:
        """Parse the LLM JSON response into TestCase models."""
        cases = []
        raw_cases = data.get("test_cases", [])

        for i, tc in enumerate(raw_cases[: self.config.max_test_cases], start=1):
            steps = [
                TestStep(
                    step_number=j,
                    action=s.get("action", ""),
                    expected_result=s.get("expected_result", ""),
                    test_data=s.get("test_data"),
                )
                for j, s in enumerate(tc.get("steps", []), start=1)
            ]

            bdd = None
            if tc.get("bdd"):
                b = tc["bdd"]
                bdd = BDDScenario(
                    given=b.get("given", []),
                    when=b.get("when", []),
                    then=b.get("then", []),
                )

            case = TestCase(
                id=tc.get("id", f"TC-{i:03d}"),
                title=tc.get("title", f"Test Case {i}"),
                description=tc.get("description", ""),
                test_type=TestType(tc.get("test_type", "functional")),
                priority=Priority(tc.get("priority", "medium")),
                preconditions=tc.get("preconditions", []),
                steps=steps,
                bdd=bdd,
                tags=tc.get("tags", []),
                estimated_duration=tc.get("estimated_duration"),
            )
            cases.append(case)

        return cases
