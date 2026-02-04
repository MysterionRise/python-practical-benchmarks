# Security Policy

## Supported Versions

| Version | Supported          | Python Versions |
| ------- | ------------------ | --------------- |
| 1.x.x   | :white_check_mark: | 3.9 - 3.14      |
| < 1.0   | :x:                | N/A             |

## Automated Security Scanning

This project employs multiple layers of automated security scanning:

### Dependency Vulnerability Scanning
- **pip-audit**: Runs on every PR and weekly to detect known vulnerabilities in dependencies
- **Dependabot**: Automatically creates PRs for dependency updates (weekly schedule)

### Static Code Analysis
- **Ruff (flake8-bandit rules)**: Security-focused linting integrated into pre-commit hooks
- **CodeQL**: GitHub's semantic code analysis for security vulnerabilities

### Secret Detection
- **detect-secrets**: Pre-commit hook to prevent accidental secret commits
- **TruffleHog**: CI/CD scanning for secrets in git history

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in this project, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Use one of these secure reporting methods:
   - [GitHub's private vulnerability reporting](https://github.com/MysterionRise/python-practical-benchmarks/security/advisories/new)
   - Email the maintainer directly (if public contact available)

### What to Include

When reporting, please provide:
- **Description**: Clear explanation of the vulnerability
- **Steps to reproduce**: Minimal steps to demonstrate the issue
- **Affected versions**: Which versions are impacted
- **Potential impact**: What could an attacker do?
- **Suggested fix**: If you have one (optional but appreciated)

### Response Timeline

- **Acknowledgment**: Within 48 hours of your report
- **Initial assessment**: Within 7 days with our evaluation
- **Resolution**: Security fixes prioritized and released ASAP
- **Credit**: Security researchers acknowledged in release notes (unless you prefer anonymity)

## Scope

### In Scope

This security policy applies to:
- Benchmark Python code (`*_perf_test.py`, `run_all_tests.py`)
- Test infrastructure (`tests/`)
- CI/CD pipeline configurations (`.github/workflows/`)
- Project configuration files (`pyproject.toml`, `requirements*.txt`)
- Dependencies specified in the project

### Out of Scope

The following are NOT security vulnerabilities for this project:
- Performance issues or benchmark inaccuracies
- Third-party dependencies (report to respective maintainers)
- Code examples in documentation (illustrative, not production code)
- Intentionally unsafe benchmark code (e.g., pickle serialization tests)

## Security Best Practices for Contributors

When contributing to this project:

### Code Security
- Run `ruff check` before committing (includes bandit security checks)
- Never commit secrets, API keys, passwords, or credentials
- Use environment variables for any sensitive configuration
- Avoid `eval()`, `exec()`, and similar dynamic execution
- Be cautious with `pickle` - document security implications when used

### Dependency Security
- Pin dependency versions in `requirements.txt`
- Check for known vulnerabilities before adding new dependencies
- Prefer well-maintained packages with active security response

### CI/CD Security
- Never disable security checks without documented justification
- Use secrets management for CI/CD credentials
- Review workflow changes carefully for injection risks

## Security-Related Configuration

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml includes:
- Ruff with bandit rules (S* checks)
- detect-secrets for credential scanning
```

### GitHub Actions

```yaml
# .github/workflows/security.yml includes:
- pip-audit dependency scanning
- TruffleHog secret scanning
- CodeQL security analysis
```

### Dependabot

```yaml
# .github/dependabot.yml:
- Weekly pip dependency updates
- Weekly GitHub Actions updates
- Grouped dev-dependency PRs
```

## Known Security Considerations

### Pickle Serialization

The `serialization_formats_perf_test.py` benchmark tests pickle performance. **Pickle is inherently insecure** when loading untrusted data. This is documented in the benchmark's decision guide:

```python
# NEVER use pickle with untrusted data - it can execute arbitrary code!
# Use JSON, MessagePack, or other safe formats for external data.
```

### File I/O

The `file_io_perf_test.py` benchmark creates temporary files. These are:
- Created in the system temp directory
- Cleaned up after benchmark completion
- Do not contain sensitive data

## Compliance

This project follows security best practices aligned with:
- OWASP Top 10 awareness
- Python security guidelines (PEP 506, etc.)
- GitHub security features and recommendations

## Updates to This Policy

This security policy may be updated as the project evolves. Check the file history for changes.

---

Thank you for helping keep this project and its users secure!
