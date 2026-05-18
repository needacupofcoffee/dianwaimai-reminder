# tests/test_remove_task.py
import os
import sys
from unittest.mock import patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import remove_task


def test_build_remove_task_command_contains_expected_values():
    assert remove_task.build_remove_task_command() == [
        "schtasks",
        "/Delete",
        "/TN",
        remove_task.TASK_NAME,
        "/F",
    ]


def test_remove_scheduled_task_runs_schtasks():
    with patch.object(remove_task, "build_remove_task_command", return_value=["schtasks", "/Delete"]), patch(
        "remove_task.subprocess.run"
    ) as mock_run:
        remove_task.remove_scheduled_task()

    mock_run.assert_called_once_with(["schtasks", "/Delete"], check=True)
