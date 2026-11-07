<div align="center">

# 🧪 AI Test Case Generator

**Generate comprehensive test cases from requirements, user stories, or feature descriptions using GPT-4**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/ai-test-case-generator.svg)](https://pypi.org/project/ai-test-case-generator/)
[![CI](https://github.com/kamranghafar/ai-test-case-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/kamranghafar/ai-test-case-generator/actions)

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [Configuration](#configuration) • [Examples](#examples) • [Contributing](#contributing)

</div>

---

## ✨ Features

- 🤖 **GPT-4 Powered** — Generates high-quality, context-aware test cases using OpenAI models
- 📝 **Multiple Input Sources** — Feed requirements as text, files (`.txt`, `.md`), or URLs
- 🎯 **8 Test Types** — Functional, edge case, negative, security, performance, usability, integration, regression
- 📋 **Flexible Output** — Markdown, JSON, or CSV formats
- 🥒 **BDD Support** — Given/When/Then scenarios alongside traditional step-based tests
- 🔗 **Platform Export** — Ready-to-import formats for **TestRail**, **Qase**, and **TestLink Pro**
- ⚙️ **Configurable** — Model, temperature, max cases, test types — all customizable
- 🖥️ **CLI + Library** — Use from the command line or import as a Python package

## 📦 Installation

```bash
pip install ai-test-case-generator
```

Or install from source:

```bash
git clone https://github.com/kamranghafar/ai-test-case-generator.git
cd ai-test-case-generator
pip install -e ".[dev]"
```

## ⚡ Quick Start

### 1. Set your OpenAI API key

```bash
export OPENAI_API_KEY="sk-..."
```

### 2. Generate test cases

```bash
# From a text requirement
ai-testgen generate "User can reset password via email"

# From a file
ai-testgen generate requirements.txt -f json -o test_cases.json

# From a URL
ai-testgen generate https://example.com/user-story

# With specific test types and BDD format
ai-testgen generate "Shopping cart checkout" -t functional -t security -t edge_case --template bdd

# Export for TestRail
ai-testgen generate spec.md --export testrail -o testrail_import.json
```

### 3. Use as a Python library

```python
from ai_test_case_generator.generator import TestGenerator
from ai_test_case_generator.models import GeneratorConfig, TestType
from ai_test_case_generator.formatters import to_markdown

config = GeneratorConfig(
    model="gpt-4",
    test_types=[TestType.FUNCTIONAL, TestType.SECURITY],
    max_test_cases=8,
    include_bdd=True,
)

gen = TestGenerator(config)
suite = gen.generate("User uploads a profile picture (JPEG/PNG, max 5MB)")

print(to_markdown(suite))
```

## 🎯 Supported Test Types

| Type | Flag | Description |
|------|------|-------------|
| Functional | `functional` | Core feature behavior verification |
| Edge Case | `edge_case` | Boundary values and unusual inputs |
| Negative | `negative` | Invalid inputs, error handling |
| Security | `security` | Auth, injection, access control |
| Performance | `performance` | Load, response time, scalability |
| Usability | `usability` | UX, accessibility, user flow |
| Integration | `integration` | Cross-component interactions |
| Regression | `regression` | Existing functionality preservation |

## 📋 Output Formats

### Markdown (default)

```bash
ai-testgen generate "Login feature" -f markdown
```

Produces a structured document with tables, preconditions, BDD scenarios, and tags.

### JSON

```bash
ai-testgen generate "Login feature" -f json -o tests.json
```

Full structured data — ideal for CI/CD pipelines and programmatic processing.

### CSV

```bash
ai-testgen generate "Login feature" -f csv -o tests.csv
```

Spreadsheet-compatible for bulk import into any test management tool.

## 🔗 Platform Export

Export directly to test management platform formats:

```bash
# TestRail (JSON for API import)
ai-testgen generate spec.md --export testrail

# Qase.io (JSON for bulk create API)
ai-testgen generate spec.md --export qase

# TestLink Pro (XML import)
ai-testgen generate spec.md --export testlink
```

## ⚙️ Configuration

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --format` | Output format: `markdown`, `json`, `csv` | `markdown` |
| `-o, --output` | Save output to file | stdout |
| `-t, --test-type` | Test types to generate (repeatable) | functional, edge_case, negative |
| `--template` | `traditional` or `bdd` | `traditional` |
| `--model` | OpenAI model name | `gpt-4` |
| `--max-cases` | Maximum test cases to generate | `10` |
| `--temperature` | LLM creativity (0.0–1.0) | `0.7` |
| `--export` | Export format: `testrail`, `qase`, `testlink` | — |
| `--api-key` | OpenAI API key (or use env var) | `$OPENAI_API_KEY` |

### Environment Variables

```bash
OPENAI_API_KEY=sk-...     # Required — your OpenAI API key
```

## 📄 Example Output

<details>
<summary>Click to see sample generated test cases</summary>

### TC-001: Verify successful password reset flow

**Type:** functional | **Priority:** critical

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click "Forgot Password" link | Password reset form displayed | — |
| 2 | Enter registered email | Email accepted | user@example.com |
| 3 | Click "Send Reset Link" | Success message shown | — |
| 4 | Open email, click reset link | "Set New Password" page displayed | — |
| 5 | Enter and confirm new password | Password accepted | NewP@ss123 |
| 6 | Click "Reset Password" | Success message, redirect to login | — |

### TC-002: Verify password complexity rejection

**Type:** negative | **Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Enter password without uppercase | Error shown | password1! |
| 2 | Enter password under 8 chars | Error shown | Pa1! |
| 3 | Enter valid password | Accepted | NewP@ss123 |

### TC-003: Verify rate limiting (Security)

**Type:** security | **Priority:** medium

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Send 5 reset requests | All succeed |
| 2 | Send 6th request within 1 hour | Rate limit error |

</details>

## 🗂️ Project Structure

```
ai-test-case-generator/
├── ai_test_case_generator/
│   ├── __init__.py          # Package metadata
│   ├── cli.py               # Click CLI interface
│   ├── generator.py         # OpenAI integration & test generation
│   ├── models.py            # Pydantic data models
│   ├── parser.py            # Input source readers (text/file/URL)
│   ├── prompts.py           # LLM prompt engineering
│   ├── formatters.py        # Output formatters (MD/JSON/CSV)
│   ├── exporters/
│   │   ├── __init__.py
│   │   └── platforms.py     # TestRail, Qase, TestLink exporters
│   └── templates/
│       └── __init__.py
├── examples/
│   ├── password_reset_requirement.txt
│   ├── sample_output.md
│   └── usage_example.py
├── tests/
│   ├── test_core.py
│   └── test_exporters.py
├── .github/workflows/ci.yml
├── pyproject.toml
├── LICENSE
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Install** dev dependencies: `pip install -e ".[dev]"`
4. **Write tests** for your changes
5. **Run** the test suite: `pytest tests/ -v`
6. **Lint**: `ruff check .` and `black .`
7. **Commit** with a clear message
8. **Push** and open a Pull Request

### Development Setup

```bash
git clone https://github.com/kamranghafar/ai-test-case-generator.git
cd ai-test-case-generator
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

## 👤 Author

**Kamran Ghaffar** — QA Engineer with 10+ years of experience building AI-powered testing tools.

- GitHub: [@kamranghafar](https://github.com/kamranghafar)

---

<div align="center">
<strong>If this tool saves you time writing test cases, give it a ⭐!</strong>
</div>
