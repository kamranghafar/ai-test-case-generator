"""Data models for test cases and configuration."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TestType(str, Enum):
    FUNCTIONAL = "functional"
    EDGE_CASE = "edge_case"
    NEGATIVE = "negative"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USABILITY = "usability"
    INTEGRATION = "integration"
    REGRESSION = "regression"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class OutputFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"
    CSV = "csv"


class TemplateFormat(str, Enum):
    TRADITIONAL = "traditional"
    BDD = "bdd"


class ExportTarget(str, Enum):
    TESTRAIL = "testrail"
    QASE = "qase"
    TESTLINK = "testlink"


class TestStep(BaseModel):
    step_number: int
    action: str
    expected_result: str
    test_data: Optional[str] = None


class BDDScenario(BaseModel):
    given: list[str]
    when: list[str]
    then: list[str]


class TestCase(BaseModel):
    id: str
    title: str
    description: str
    test_type: TestType
    priority: Priority
    preconditions: list[str] = Field(default_factory=list)
    steps: list[TestStep] = Field(default_factory=list)
    bdd: Optional[BDDScenario] = None
    tags: list[str] = Field(default_factory=list)
    estimated_duration: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TestSuite(BaseModel):
    title: str
    requirement: str
    test_cases: list[TestCase] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    model_used: str = ""
    total_count: int = 0

    def model_post_init(self, __context):
        self.total_count = len(self.test_cases)

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    def to_dict(self) -> dict:
        return self.model_dump()


class GeneratorConfig(BaseModel):
    api_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    test_types: list[TestType] = Field(
        default_factory=lambda: [TestType.FUNCTIONAL, TestType.EDGE_CASE, TestType.NEGATIVE]
    )
    template_format: TemplateFormat = TemplateFormat.TRADITIONAL
    output_format: OutputFormat = OutputFormat.MARKDOWN
    max_test_cases: int = 10
    include_bdd: bool = False
    language: str = "en"
