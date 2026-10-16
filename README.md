# hc-data-skills

Free, open-source agent skills for healthcare data engineering teams. Format-compatible with [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) and [Cursor](https://docs.cursor.com/context/rules-for-ai) skills — one folder per skill with a `SKILL.md` that has name + description frontmatter, when-to-use, steps, plus scripts and fixtures.

**Your data stays local. We never host your data. No BAA needed.**

Teams install skills into **their own repo**; all memory and working files live as files in the team's repository. There is no hosted service, no data upload, and no external API calls.

---

## Quick Start

```bash
# Install the CLI (requires Python 3.10+)
pipx install hc-data-skills
# or
uv pip install hc-data-skills

# Install skills into your repo
cd your-data-repo/
hcskills install --target cursor   # copies to .cursor/skills/hc-data-skills/
hcskills install --target claude   # copies to .claude/skills/hc-data-skills/

# List available skills
hcskills list

# Initialize a local memory folder
hcskills memory init

# Scan files for PHI patterns
hcskills guard path/to/file.csv

# Scan git staged files (pre-commit)
hcskills guard --staged
```

## Free Skills

| Skill | Description |
|-------|-------------|
| `hl7v2-parse` | Parse HL7v2 ADT and ORU messages into flat, analysis-ready tables (CSV/JSON). |
| `phi-column-scan` | Scan a schema, dbt model, or sample data to flag columns that likely contain PHI — runs entirely locally. |
| `pipeline-runbook` | Generate an on-call runbook from an Airflow DAG or dbt job manifest. |

## Team Tier

A **Team** tier with 7 more skills is available separately:

`834-file-check`, `fhir-mapping`, `deid-pass`, `member-match`, `dbt-healthcare-conventions`, `roster-reconcile`, `code-set-lookup`.

**Contact for access.**

## PHI Guard

The PHI guard scans files for HIPAA-sensitive patterns (SSN, MRN, DOB+name, phone, email, addresses) and blocks commits when matches are found.

### As a CLI command

```bash
hcskills guard file1.csv file2.json
hcskills guard --staged  # scan git staged files
```

### As a pre-commit hook

Copy the hook into your repo:

```bash
cp $(pip show hc-data-skills | grep Location | cut -d' ' -f2)/hcskills/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### False positive suppression

Add `# phi-safe` as an inline comment to suppress a match on a specific line.

## Memory

The `hcskills memory init` command creates a local `memory/` folder template:

```
memory/
├── decisions/         # Data engineering decision records
├── column-glossary/   # Source-to-canonical column mappings
└── gotchas/           # Known data quality issues and vendor quirks
```

Memory lives in **your repo** — it's never uploaded anywhere. The PHI guard automatically scans `memory/` to prevent accidental PHI commits.

## Architecture & Data Privacy

- **No hosted service**: The CLI copies skill files into your repo's `.cursor/skills/` or `.claude/skills/` directory. That's it.
- **No data transmission**: All scripts run locally. No API calls, no telemetry, no data upload.
- **No BAA needed**: Since we never touch your data, there's no covered entity relationship.
- **Memory is local**: Decision records, column glossaries, and gotchas live as files in your repo.

## License

MIT — see [LICENSE](LICENSE).

## Development

```bash
git clone https://github.com/blacktj/hc-data-skills.git
cd hc-data-skills
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check src/ tests/
```

## Contributing

1. All fixtures must use **synthetic, obviously fake data**. No real PHI, ever.
2. Each skill must have a working script and at least one fixture test.
