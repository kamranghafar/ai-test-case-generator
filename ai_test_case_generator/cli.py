"""CLI interface for ai-test-case-generator."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import __version__
from .formatters import to_csv, to_json, to_markdown
from .models import (
    ExportTarget,
    GeneratorConfig,
    OutputFormat,
    TemplateFormat,
    TestType,
)
from .parser import read_requirement

console = Console()

VALID_TEST_TYPES = [t.value for t in TestType]


@click.group()
@click.version_option(version=__version__, prog_name="ai-testgen")
def cli():
    """🧪 AI Test Case Generator — Generate test cases from requirements using GPT-4."""
    pass


@cli.command()
@click.argument("source")
@click.option(
    "-o", "--output", "output_file",
    type=click.Path(),
    help="Write output to a file instead of stdout.",
)
@click.option(
    "-f", "--format", "fmt",
    type=click.Choice(["markdown", "json", "csv"]),
    default="markdown",
    help="Output format (default: markdown).",
)
@click.option(
    "-t", "--test-type",
    multiple=True,
    type=click.Choice(VALID_TEST_TYPES),
    help="Test types to generate (can specify multiple). Default: functional, edge_case, negative.",
)
@click.option(
    "--template",
    type=click.Choice(["traditional", "bdd"]),
    default="traditional",
    help="Test case template format.",
)
@click.option(
    "--model",
    default="gpt-4",
    help="OpenAI model to use (default: gpt-4).",
)
@click.option(
    "--max-cases",
    default=10,
    type=int,
    help="Maximum number of test cases to generate (default: 10).",
)
@click.option(
    "--api-key",
    envvar="OPENAI_API_KEY",
    help="OpenAI API key (or set OPENAI_API_KEY env var).",
)
@click.option(
    "--temperature",
    default=0.7,
    type=float,
    help="LLM temperature 0.0–1.0 (default: 0.7).",
)
@click.option(
    "--export",
    "export_target",
    type=click.Choice(["testrail", "qase", "testlink"]),
    help="Export to a test management platform format.",
)
@click.option("--title", help="Custom test suite title.")
def generate(
    source: str,
    output_file: str | None,
    fmt: str,
    test_type: tuple[str, ...],
    template: str,
    model: str,
    max_cases: int,
    api_key: str | None,
    temperature: float,
    export_target: str | None,
    title: str | None,
):
    """Generate test cases from a requirement SOURCE.

    SOURCE can be:

    \b
      • A plain text requirement in quotes
      • A path to a .txt/.md file
      • A URL to a requirements page

    Examples:

    \b
      ai-testgen generate "User can reset password via email"
      ai-testgen generate requirements.md -f json -o tests.json
      ai-testgen generate https://example.com/story -t security -t negative
      ai-testgen generate spec.txt --template bdd --export testrail
    """
    # Parse test types
    if test_type:
        types = [TestType(t) for t in test_type]
    else:
        types = [TestType.FUNCTIONAL, TestType.EDGE_CASE, TestType.NEGATIVE]

    include_bdd = template == "bdd"

    config = GeneratorConfig(
        api_key=api_key,
        model=model,
        temperature=temperature,
        test_types=types,
        template_format=TemplateFormat(template),
        output_format=OutputFormat(fmt),
        max_test_cases=max_cases,
        include_bdd=include_bdd,
    )

    # Read the requirement
    console.print(Panel("🧪 AI Test Case Generator", style="bold cyan"))
    with Progress(SpinnerColumn(), TextColumn("[bold blue]{task.description}"), console=console) as progress:
        task = progress.add_task("Reading requirement...", total=None)
        try:
            requirement = read_requirement(source)
        except Exception as e:
            console.print(f"[red]Error reading source:[/red] {e}")
            sys.exit(1)

        if not requirement.strip():
            console.print("[red]Empty requirement. Nothing to generate.[/red]")
            sys.exit(1)

        progress.update(task, description=f"Generating test cases with {model}...")

        from .generator import TestGenerator

        try:
            gen = TestGenerator(config)
            suite = gen.generate(requirement, title=title)
        except Exception as e:
            console.print(f"[red]Generation failed:[/red] {e}")
            sys.exit(1)

    console.print(f"[green]✓[/green] Generated {suite.total_count} test cases\n")

    # Handle export target
    if export_target:
        from .exporters.platforms import to_qase_json, to_testrail_json, to_testlink_xml

        export_funcs = {
            "testrail": to_testrail_json,
            "qase": to_qase_json,
            "testlink": to_testlink_xml,
        }
        output = export_funcs[export_target](suite)
        ext = "xml" if export_target == "testlink" else "json"
        if not output_file:
            output_file = f"test_cases_{export_target}.{ext}"
    else:
        format_funcs = {
            "markdown": to_markdown,
            "json": to_json,
            "csv": to_csv,
        }
        output = format_funcs[fmt](suite)

    if output_file:
        Path(output_file).write_text(output, encoding="utf-8")
        console.print(f"[green]✓[/green] Saved to {output_file}")
    else:
        console.print(output)


@cli.command()
def config():
    """Show current configuration and environment status."""
    api_key = os.getenv("OPENAI_API_KEY")
    masked = f"{api_key[:8]}...{api_key[-4:]}" if api_key and len(api_key) > 12 else "NOT SET"
    console.print(Panel("⚙️  Configuration", style="bold cyan"))
    console.print(f"  OPENAI_API_KEY : {masked}")
    console.print(f"  Default model  : gpt-4")
    console.print(f"  Version        : {__version__}")


@cli.command()
def test_types():
    """List all available test types."""
    console.print(Panel("📋 Available Test Types", style="bold cyan"))
    for t in TestType:
        console.print(f"  • {t.value}")


if __name__ == "__main__":
    cli()
