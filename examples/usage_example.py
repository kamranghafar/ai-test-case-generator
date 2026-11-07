"""Example: Using ai-test-case-generator as a Python library.

Set OPENAI_API_KEY before running:
    export OPENAI_API_KEY="sk-..."
    python examples/usage_example.py
"""

from ai_test_case_generator.generator import TestGenerator
from ai_test_case_generator.models import (
    GeneratorConfig,
    OutputFormat,
    TemplateFormat,
    TestType,
)
from ai_test_case_generator.formatters import to_markdown, to_json
from ai_test_case_generator.exporters.platforms import to_testrail_json


def main():
    # Configure the generator
    config = GeneratorConfig(
        model="gpt-4",
        temperature=0.7,
        test_types=[TestType.FUNCTIONAL, TestType.EDGE_CASE, TestType.SECURITY],
        template_format=TemplateFormat.BDD,
        include_bdd=True,
        max_test_cases=8,
    )

    # Create the generator
    gen = TestGenerator(config)

    # Generate from a requirement string
    requirement = """
    As a user, I want to upload a profile picture so that other users can
    identify me visually.

    - Supported formats: JPEG, PNG, GIF
    - Maximum file size: 5 MB
    - Image is cropped to square (1:1 ratio)
    - Minimum dimensions: 100x100 pixels
    - Maximum dimensions: 4000x4000 pixels
    """

    suite = gen.generate(requirement, title="Profile Picture Upload Tests")

    # Output as Markdown
    print(to_markdown(suite))

    # Or export for TestRail
    testrail_data = to_testrail_json(suite)
    with open("testrail_import.json", "w") as f:
        f.write(testrail_data)
    print(f"\nTestRail import file saved ({len(suite.test_cases)} cases)")


if __name__ == "__main__":
    main()
