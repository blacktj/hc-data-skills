"""hcskills CLI — install, update, list, memory, and guard commands."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import click

from hcskills import __version__
from hcskills.guard import scan_paths

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"

SKILLS: dict[str, str] = {
    "hl7v2-parse": "Parse HL7v2 ADT/ORU messages into flat tables",
    "phi-column-scan": "Flag likely PHI columns from schema/samples",
    "pipeline-runbook": "Generate on-call runbooks from Airflow/dbt",
}


def _resolve_target(target: str) -> Path:
    targets = {
        "cursor": Path(".cursor/skills/hc-data-skills"),
        "claude": Path(".claude/skills/hc-data-skills"),
    }
    return targets[target]


@click.group()
@click.version_option(__version__, prog_name="hcskills")
def cli() -> None:
    """hc-data-skills — free agent skills for healthcare data engineering."""


@cli.command()
@click.option(
    "--target",
    type=click.Choice(["cursor", "claude"]),
    default="cursor",
    help="Where to install skills (default: cursor).",
)
def install(target: str) -> None:
    """Copy skills into the current repo's skills directory."""
    dest = _resolve_target(target)
    installed = 0
    for slug in sorted(SKILLS):
        src = SKILLS_DIR / slug
        if not src.exists():
            click.echo(f"  WARN  {slug} source not found at {src}")
            continue
        skill_dest = dest / slug
        if skill_dest.exists():
            shutil.rmtree(skill_dest)
        shutil.copytree(
            src, skill_dest,
            ignore=shutil.ignore_patterns("fixtures", "__pycache__"),
        )
        click.echo(f"  OK    {slug}")
        installed += 1
    click.echo(f"\nInstalled {installed} skills to {dest}/")


@cli.command()
@click.option(
    "--target",
    type=click.Choice(["cursor", "claude"]),
    default="cursor",
    help="Where skills are installed (default: cursor).",
)
def update(target: str) -> None:
    """Re-install skills (same as install, overwrites existing)."""
    ctx = click.get_current_context()
    ctx.invoke(install, target=target)


@cli.command(name="list")
def list_skills() -> None:
    """List available skills."""
    click.echo(f"{'Skill':<25} {'Description'}")
    click.echo("-" * 65)
    for slug, desc in sorted(SKILLS.items()):
        click.echo(f"{slug:<25} {desc}")
    click.echo(
        "\nTeam tier (7 additional skills) available separately — "
        "contact for access."
    )


@cli.group()
def memory() -> None:
    """Manage the local memory/ folder."""


@memory.command(name="init")
def memory_init() -> None:
    """Create a memory/ folder template in the current repo."""
    base = Path("memory")
    templates: dict[str, str] = {
        "decisions/README.md": (
            "# Decisions\n\n"
            "Record data-engineering decisions here.\n"
            "Format: one Markdown file per decision, "
            "named `YYYY-MM-DD-<slug>.md`.\n"
        ),
        "column-glossary/README.md": (
            "# Column Glossary\n\n"
            "Map source columns to canonical names.\n"
            "Use CSV or Markdown tables. One file per source system.\n"
        ),
        "gotchas/README.md": (
            "# Gotchas\n\n"
            "Document known data quality issues, vendor quirks, "
            "and edge cases.\n"
        ),
    }
    created = 0
    for rel_path, content in templates.items():
        fp = base / rel_path
        if fp.exists():
            click.echo(f"  EXISTS  {fp}")
            continue
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        click.echo(f"  CREATE  {fp}")
        created += 1
    click.echo(
        f"\nMemory folder ready at {base}/ ({created} files created)"
    )


@cli.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--staged", is_flag=True,
    help="Scan git staged files instead of explicit paths.",
)
def guard(paths: tuple[str, ...], staged: bool) -> None:
    """Scan files for PHI patterns and block if found."""
    import subprocess

    file_list: list[Path] = []
    if staged:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            capture_output=True,
            text=True,
        )
        file_list = [
            Path(f) for f in result.stdout.strip().splitlines() if f
        ]
    else:
        file_list = [Path(p) for p in paths]

    if not file_list:
        click.echo("No files to scan.")
        sys.exit(0)

    findings = scan_paths(file_list)
    if findings:
        click.echo("PHI DETECTED — commit blocked\n")
        for finding in findings:
            click.echo(f"  {finding['file']}:{finding['line']}")
            click.echo(f"    Pattern: {finding['pattern_name']}")
            click.echo(f"    Match:   {finding['match']}")
            click.echo()
        click.echo(
            "Remove or redact the flagged content before committing.\n"
            "If this is a false positive, add a "
            "# phi-safe comment on that line."
        )
        sys.exit(1)
    else:
        click.echo(
            f"No PHI patterns found in {len(file_list)} file(s)."
        )
        sys.exit(0)
