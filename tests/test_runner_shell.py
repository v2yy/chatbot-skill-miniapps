from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).parents[1]
RUNNER_SCRIPT = REPOSITORY_ROOT / "skills" / "xiaocx-miniapp" / "scripts" / "runner.sh"


class RunnerShellTest(unittest.TestCase):
    def test_bundled_runner_ignores_an_older_home_directory_clone(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_home = Path(temporary_directory)
            old_clone_runner = (
                temporary_home / "chatbot-skill-miniapps" / "tools" / "run_miniapp.py"
            )
            old_clone_runner.parent.mkdir(parents=True)
            old_clone_runner.write_text(
                "import json\nprint(json.dumps({'source': 'old-clone'}))\n",
                encoding="utf-8",
            )
            old_clone_python = (
                temporary_home / "chatbot-skill-miniapps" / ".venv" / "bin" / "python"
            )
            old_clone_python.parent.mkdir(parents=True)
            old_clone_python.symlink_to(sys.executable)

            completed = subprocess.run(
                ["bash", str(RUNNER_SCRIPT), "--list"],
                capture_output=True,
                check=True,
                env={"HOME": str(temporary_home), "PATH": os.environ["PATH"]},
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertNotEqual("old-clone", payload.get("source"))
        self.assertTrue(payload.get("ok"))
        self.assertIn("摸头", payload["commands"])
