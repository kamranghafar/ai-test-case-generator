"""Tests for exporters."""

import json
import xml.etree.ElementTree as ET

from ai_test_case_generator.exporters.platforms import (
    to_qase_json,
    to_testrail_json,
    to_testlink_xml,
)
from ai_test_case_generator.models import (
    Priority,
    TestCase,
    TestStep,
    TestSuite,
    TestType,
)


def _make_suite():
    tc = TestCase(
        id="TC-001",
        title="Test login",
        description="Verify login works",
        test_type=TestType.FUNCTIONAL,
        priority=Priority.HIGH,
        steps=[
            TestStep(step_number=1, action="Enter credentials", expected_result="Accepted"),
        ],
        tags=["login"],
    )
    return TestSuite(
        title="Login Tests",
        requirement="Login feature",
        test_cases=[tc],
        model_used="gpt-4",
    )


def test_testrail_export():
    output = to_testrail_json(_make_suite())
    data = json.loads(output)
    assert "cases" in data
    assert data["cases"][0]["title"] == "Test login"
    assert data["cases"][0]["priority_id"] == 3  # high


def test_qase_export():
    output = to_qase_json(_make_suite())
    data = json.loads(output)
    assert "cases" in data
    assert len(data["cases"][0]["steps"]) == 1


def test_testlink_export():
    output = to_testlink_xml(_make_suite())
    assert "testcase" in output
    assert "Test login" in output
