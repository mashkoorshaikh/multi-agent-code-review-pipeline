# Security Policy

The **Multi-Agent Code Review & Debugging Pipeline** analyzes untrusted code and automates developer workflows. Security is a first-class requirement across our entire architecture.

---

## Reporting a Security Vulnerability

If you discover a security vulnerability, **please do NOT open a public GitHub issue**. Instead, follow responsible disclosure practices:

1. **Email:** Contact the project maintainer directly at **mashkoorshaikh.dev@gmail.com** (or via GitHub Private Vulnerability Reporting).
2. **Details to Include:**
   - Detailed description of the vulnerability.
   - Proof of concept (PoC) or reproduction steps.
   - Potential impact on the host system, repository, or credentials.
   - Suggested remediation (if known).
3. **Response Timeline:**
   - Acknowledgement within 48 hours.
   - Status update with assessment and mitigation plan within 5 business days.
   - Coordinated release of security patches before public disclosure.

---

## Supported Versions

| Version / Branch | Supported | Notes |
| :--- | :--- | :--- |
| `master` | Yes | Active development and latest security patches |
| Releases (< 1.0) | Yes | Current pre-release / milestone tags |

---

## Core Security Model & Trust Boundaries

Our review pipeline operates under strict defensive boundaries when handling untrusted pull requests:

### 1. Static Analysis Isolation
- **No Untrusted Configuration Loading (`SEC-01` & `SEC-02`):** Ruff runs with `--isolated`, and Bandit discovers configuration strictly from maintainer-controlled directories. Scanned repositories cannot override security rules or suppress diagnostics via malicious `pyproject.toml`, `bandit.yaml`, or `.bandit` files.
- **AST-Only Processing:** Static linters inspect source files as passive text/AST; untrusted code is never imported or executed during static analysis.

### 2. Docker Sandbox Isolation
- **Dynamic Execution Boundary:** When AI agents generate unit tests or verify bug fixes, execution occurs strictly inside an ephemeral Docker container.
- **Container Restrictions:**
  - `--network=none` (zero outbound or inbound network access).
  - `--read-only` (read-only root filesystem).
  - Unprivileged non-root user (`appuser`, UID 1000).
  - Strict resource limits: 256 MB memory, 1.0 CPU, 64 process limit (PIDs limit).
  - No capability additions (`--cap-drop=ALL`).

### 3. Credential & Token Protection
- **No CLI Token Arguments (`SEC-03`):** GitHub tokens cannot be passed via `--token` CLI arguments to prevent exposure in process trees, shell history, and logs.
- **Redaction Engine:** All resolved credentials (`GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN_FILE`) are registered with the token redaction engine and masked across console logs, exceptions, and error output.
- **Memory Limits (`SEC-04`):** Remote pull request diff downloads enforce a strict 20 MB streaming ceiling to guard against resource exhaustion.

### 4. Human Approval Gate
- **No Unconditional Writes:** The automated review pipeline defaults to `COMMENT` or read-only preview mode. It never presumes authority to merge pull requests or publish comments without human review and approval.
- **Plan Hash Verification:** Approval is cryptographically bound to the SHA-256 fingerprint of the reviewed plan and verified against the live PR head commit SHA within a 600-second TTL.

### 5. GitHub Actions Least Privilege
- The automated PR review workflow requests only `contents: read` and `pull-requests: read`.
- It executes strictly from the trusted base branch checkout to prevent untrusted pull request code from modifying workflow execution or accessing secrets.

