"""Output formatters — render a TestSuite as Markdown, JSON, or CSV."""

from __future__ import annotations

import csv
import io
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import TestSuite


def to_markdown(suite: "TestSuite") -> str:
    """Render the test suite as Markdown."""
    lines: list[str] = []
    lines.append(f"# {suite.title}\n")
    lines.append(f"**Requirement:** {suite.requirement}\n")
    lines.append(f"**Generated:** {suite.generated_at}  ")
    lines.append(f"**Model:** {suite.model_used}  ")
    lines.append(f"**Total Test Cases:** {suite.total_count}\n")
    lines.append("---\n")

    for tc in suite.test_cases:
        lines.append(f"## {tc.id}: {tc.title}\n")
        lines.append(f"**Type:** {tc.test_type.value} | **Priority:** {tc.priority.value}")
        if tc.estimated_duration:
            lines.append(f" | **Est. Duration:** {tc.estimated_duration}")
        lines.append("\n")
        lines.append(f"> {tc.description}\n")

        if tc.preconditions:
            lines.append("### Preconditions\n")
            for pre in tc.preconditions:
                lines.append(f"- {pre}")
            lines.append("")

        if tc.steps:
            lines.append("### Steps\n")
            lines.append("| # | Action | Expected Result | Test Data |")
            lines.append("|---|--------|-----------------|-----------|")
            for s in tc.steps:
                data = s.test_data or "—"
                lines.append(f"| {s.step_number} | {s.action} | {s.expected_result} | {data} |")
            lines.append("")

        if tc.bdd:
            lines.append("### BDD Scenario\n")
            lines.append("```gherkin")
            for g in tc.bdd.given:
                lines.append(f"Given {g}")
            for w in tc.bdd.when:
                lines.append(f"When {w}")
            for t in tc.bdd.then:
                lines.append(f"Then {t}")
            lines.append("```\n")

        if tc.tags:
            lines.append(f"**Tags:** {', '.join(tc.tags)}\n")

        lines.append("---\n")

    return "\n".join(lines)


def to_json(suite: "TestSuite") -> str:
    """Render the test suite as formatted JSON."""
    return suite.to_json()


def to_csv(suite: "TestSuite") -> str:
    """Render the test suite as CSV."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "ID", "Title", "Description", "Type", "Priority",
        "Preconditions", "Steps", "Tags", "Est. Duration",
    ])

    for tc in suite.test_cases:
        preconditions = "; ".join(tc.preconditions)
        steps_text = " | ".join(
            f"{s.step_number}. {s.action} -> {s.expected_result}" for s in tc.steps
        )
        tags = ", ".join(tc.tags)
        writer.writerow([
            tc.id, tc.title, tc.description, tc.test_type.value,
            tc.priority.value, preconditions, steps_text, tags,
            tc.estimated_duration or "",
        ])

    return buf.getvalue()
