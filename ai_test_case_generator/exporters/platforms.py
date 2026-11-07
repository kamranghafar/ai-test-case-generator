"""Export test suites to TestRail, Qase, and TestLink Pro formats."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import TestSuite


def to_testrail_json(suite: "TestSuite") -> str:
    """Export to TestRail-compatible JSON for API import.

    Compatible with TestRail API v2 — POST index.php?/api/v2/add_case/{section_id}
    """
    cases = []
    priority_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    type_map = {
        "functional": 1, "edge_case": 6, "negative": 7, "security": 8,
        "performance": 9, "usability": 10, "integration": 3, "regression": 4,
    }

    for tc in suite.test_cases:
        steps_separated = [
            {"content": s.action, "expected": s.expected_result}
            for s in tc.steps
        ]
        case = {
            "title": tc.title,
            "custom_preconds": "\n".join(tc.preconditions),
            "custom_steps_separated": steps_separated,
            "priority_id": priority_map.get(tc.priority.value, 2),
            "type_id": type_map.get(tc.test_type.value, 1),
            "estimate": tc.estimated_duration or "5m",
            "refs": tc.id,
        }
        cases.append(case)

    return json.dumps({"cases": cases}, indent=2)


def to_qase_json(suite: "TestSuite") -> str:
    """Export to Qase.io bulk create format.

    Compatible with Qase API v1 — POST /v1/case/{project_code}/bulk
    """
    cases = []
    severity_map = {"critical": 1, "high": 2, "medium": 3, "low": 4}

    for tc in suite.test_cases:
        steps = [
            {
                "position": s.step_number,
                "action": s.action,
                "expected_result": s.expected_result,
                "data": s.test_data or "",
            }
            for s in tc.steps
        ]
        case = {
            "title": tc.title,
            "description": tc.description,
            "preconditions": "\n".join(tc.preconditions),
            "severity": severity_map.get(tc.priority.value, 3),
            "type": 1,  # Functional
            "is_flaky": 0,
            "steps": steps,
            "tags": tc.tags,
        }
        cases.append(case)

    return json.dumps({"cases": cases}, indent=2)


def to_testlink_xml(suite: "TestSuite") -> str:
    """Export to TestLink Pro XML import format."""
    root = ET.Element("testsuite", name=suite.title)

    for tc in suite.test_cases:
        tc_elem = ET.SubElement(root, "testcase", name=tc.title)

        summary = ET.SubElement(tc_elem, "summary")
        summary.text = f"<![CDATA[{tc.description}]]>"

        preconditions_elem = ET.SubElement(tc_elem, "preconditions")
        preconditions_elem.text = f"<![CDATA[{'<br/>'.join(tc.preconditions)}]]>"

        steps_elem = ET.SubElement(tc_elem, "steps")
        for s in tc.steps:
            step_elem = ET.SubElement(steps_elem, "step")
            step_num = ET.SubElement(step_elem, "step_number")
            step_num.text = str(s.step_number)
            actions = ET.SubElement(step_elem, "actions")
            actions.text = f"<![CDATA[{s.action}]]>"
            expected = ET.SubElement(step_elem, "expectedresults")
            expected.text = f"<![CDATA[{s.expected_result}]]>"
            exec_type = ET.SubElement(step_elem, "execution_type")
            exec_type.text = "1"  # Manual

        importance_map = {"critical": "3", "high": "3", "medium": "2", "low": "1"}
        importance = ET.SubElement(tc_elem, "importance")
        importance.text = importance_map.get(tc.priority.value, "2")

        kw_elem = ET.SubElement(tc_elem, "keywords")
        for tag in tc.tags:
            kw = ET.SubElement(kw_elem, "keyword", name=tag)

    return ET.tostring(root, encoding="unicode", xml_declaration=True)
