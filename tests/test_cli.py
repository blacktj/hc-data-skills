"""Tests for the hcskills CLI."""

from click.testing import CliRunner

from hcskills.cli import SKILLS, cli


class TestCli:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0." in result.output

    def test_list(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "hl7v2-parse" in result.output
        assert "phi-column-scan" in result.output
        assert "pipeline-runbook" in result.output
        assert "contact for access" in result.output.lower()
        table_rows = [
            line for line in result.output.splitlines()
            if line.split() and line.split()[0] in SKILLS
        ]
        assert len(table_rows) == len(SKILLS)

    def test_memory_init(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["memory", "init"])
            assert result.exit_code == 0
            assert "CREATE" in result.output

    def test_guard_no_files(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["guard"])
        assert result.exit_code == 0
        assert "No files" in result.output

    def test_guard_clean_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("clean.csv", "w") as f:
                f.write("code,value\nE11.9,test\n")
            result = runner.invoke(cli, ["guard", "clean.csv"])
            assert result.exit_code == 0
            assert "No PHI" in result.output

    def test_guard_phi_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("phi.csv", "w") as f:
                f.write("name,ssn\nFake,987-65-4320\n")
            result = runner.invoke(cli, ["guard", "phi.csv"])
            assert result.exit_code == 1
            assert "PHI DETECTED" in result.output
