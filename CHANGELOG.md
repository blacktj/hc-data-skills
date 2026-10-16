# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-16

### Added

- Initial public free-tier release of hc-data-skills (MIT).
- Three free skills: `hl7v2-parse`, `phi-column-scan`, `pipeline-runbook`.
- `hcskills` CLI with `install`, `update`, `list`, `memory init`, and `guard` commands.
- PHI guard: pre-commit hook and `hcskills guard` for scanning files for HIPAA-sensitive patterns.
- Synthetic fixtures and tests for every free skill.
- GitHub Actions CI for lint and tests.
