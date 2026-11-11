## Description
Briefly describe the purpose of this PR and the changes introduced.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Security remediation or hardening

## Verification & Testing
Describe the tests you ran to verify your changes:
- [ ] Unit tests added / updated
- [ ] Full test suite passed (`python -m pytest -q`)
- [ ] Ruff lint checks passed (`ruff check .`)
- [ ] Bandit security scan passed (`bandit -c bandit.yaml -r .`)
- [ ] Git diff hygiene verified (`git diff --check`)

## Security Checklist
- [ ] No API keys, credentials, or personal secrets are included.
- [ ] Untrusted repository input cannot control scanner configuration or escape sandbox boundaries.
- [ ] Backward compatibility is preserved where applicable.

