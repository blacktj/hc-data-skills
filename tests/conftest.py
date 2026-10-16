"""Shared test configuration — adds skill script dirs to sys.path."""

import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"

SKILL_SCRIPT_DIRS = [
    SKILLS_ROOT / "hl7v2-parse" / "scripts",
    SKILLS_ROOT / "phi-column-scan" / "scripts",
    SKILLS_ROOT / "pipeline-runbook" / "scripts",
]

for d in SKILL_SCRIPT_DIRS:
    path_str = str(d)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
