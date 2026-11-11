# Contributing to Multi-Agent Code Review & Debugging Pipeline

Thank you for your interest in contributing to the **Multi-Agent Code Review & Debugging Pipeline**! This project is an open-source developer tool designed to provide automated, safe, and transparent code review and verification.

We welcome contributions from the community—whether reporting bugs, improving documentation, submitting feature enhancements, or adding new static analysis or agent capabilities.

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please be respectful, constructive, and collaborative in all discussions and pull requests.

---

## Getting Started

### 1. Prerequisites
- **Python 3.10+** (Python 3.11+ recommended)
- **Git**
- Optional: **Docker** (required only for dynamic sandboxed test execution)
- Optional: **Ollama** or **OpenAI API key** (for local or cloud AI agents; deterministic scanning works without credentials)

### 2. Fork and Clone
```bash
git clone https://github.com/<your-username>/multi-agent-code-review-pipeline.git
cd multi-agent-code-review-pipeline
```

### 3. Create a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)
```bash
cp .env.example .env
```
Edit `.env` to configure your preferred AI provider (OpenAI, Ollama, or OpenAI-compatible endpoint) if you plan to work on AI-assisted agent features.

---

## Development & Testing Workflow

Before submitting a pull request, verify that your changes pass all project standards.

### 1. Run the Full Test Suite
```bash
python -m pytest -q
```
Ensure all tests pass and no regression tests are weakened.

### 2. Run Linting & Formatting Checks
```bash
ruff check .
```
Fix any auto-fixable issues with `ruff check --fix .` if appropriate, ensuring documentation and comments are preserved.

### 3. Run Security Scan
```bash
bandit -c bandit.yaml -r .
```
Verify that no high- or medium-severity security issues are introduced.

### 4. Verify Git Diff Hygiene
```bash
git diff --check
```
Ensure there are no trailing whitespace errors, leftover debug code, or unresolved conflict markers.

---

## Contribution Guidelines & Principles

1. **Security-First Mindset:**
   - Untrusted repository code or PR inputs must never be executed on the host. Dynamic execution must remain restricted to the Docker sandbox (`--network=none`, `--read-only`, non-root user).
   - Scanner configurations must never be loaded from untrusted PR checkouts.
   - Tokens and credentials must always be registered with the redaction filter.
2. **Deterministic Scans Work Without Paid Keys:**
   - Basic static analysis (Ruff, Bandit, AST Semantic Analyzer) must remain 100% operational with zero credentials.
3. **Preserve Human-in-the-Loop Safeguards:**
   - No automated agent or LLM output should ever possess authority to merge, write, or comment on pull requests without human review and approval.
4. **Comprehensive Test Coverage:**
   - Every bugfix must include regression tests.
   - Every new feature must include targeted unit and integration tests.

---

## Submitting Pull Requests

1. Create a dedicated branch for your change:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
2. Commit your changes with clear, descriptive commit messages.
3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a pull request against the `master` branch. Fill out the provided pull request template thoroughly.

Thank you for helping make this developer tool more robust, secure, and useful!

