from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).parents[1]
RUNNER_PATH = REPOSITORY_ROOT / "tools" / "run_miniapp.py"


def _load_runner_module():
    spec = importlib.util.spec_from_file_location("run_miniapp_test", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RunMiniappTest(unittest.TestCase):
    def test_local_image_markdown_becomes_an_image_source(self) -> None:
        runner = _load_runner_module()
        self.assertTrue(hasattr(runner, "split_miniapp_output"))

        text, image_sources = runner.split_miniapp_output(
            "![摸头](/private/var/folders/example/petpet_10001.gif)"
        )

        self.assertEqual("", text)
        self.assertEqual(
            ["/private/var/folders/example/petpet_10001.gif"], image_sources
        )
