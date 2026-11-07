"""Unit tests for models and formatters."""

import json

from ai_test_case_generator.formatters import to_csv, to_json, to_markdown
from ai_test_case_generator.models import (
    BDDScenario,
    GeneratorConfig,
    OutputFormat,
    Priority,
    TemplateFormat,
    TestCase,
    TestStep,
    TestSuite,
    TestType,
)


def _make_suite() -> TestSuite:
    """Create a sample test suite for testing."""
    tc = TestCase(
        id="TC-001",
        title="Verify login with valid credentials",
        description="Test that a user can log in with correct username and password",
        test_type=TestType.FUNCTIONAL,
        priority=Priority.HIGH,
        preconditions=["User account exists", "User is on login page"],
        steps=[
            TestStep(step_number=1, action="Enter valid username", expected_result="Username accepted", test_data="testuser@example.com"),
            TestStep(step_number=2, action="Enter valid password", expected_result="Password field masked"),
            TestStep(step_number=3, action="Click Login button", expected_result="User redirected to dashboard"),
        ],
        bdd=BDDScenario(
            given=["user has a valid account"],
            when=["user enters correct credentials and clicks Login"],
            then=["user is redirected to the dashboard"],
        ),
        tags=["login", "authentication", "smoke"],
        estimated_duration="2 min",
    )
    return TestSuite(
        title="Login Feature Tests",
        requirement="User should be able to log in with email and password",
        test_cases=[tc],
        model_used="gpt-4",
    )


def test_test_suite_count():
    suite = _make_suite()
    assert suite.total_count == 1


def test_to_markdown():
    md = to_markdown(_make_suite())
    assert "# Login Feature Tests" in md
    assert "TC-001" in md
    assert "Verify login with valid credentials" in md
    assert "Given" in md  # BDD section


def test_to_json():
    raw = to_json(_make_suite())
    data = json.loads(raw)
    assert data["title"] == "Login Feature Tests"
    assert len(data["test_cases"]) == 1


def test_to_csv():
    output = to_csv(_make_suite())
    assert "TC-001" in output
    assert "Verify login with valid credentials" in output


def test_config_defaults():
    cfg = GeneratorConfig()
    assert cfg.model == "gpt-4"
    assert cfg.temperature == 0.7
    assert cfg.output_format == OutputFormat.MARKDOWN
    assert cfg.template_format == TemplateFormat.TRADITIONAL
    assert TestType.FUNCTIONAL in cfg.test_types


def test_parser_raw_text():
    from ai_test_case_generator.parser import read_requirement
    text = "User can reset their password"
    assert read_requirement(text) == text
