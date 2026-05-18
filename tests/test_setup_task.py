import os
import sys
from unittest.mock import patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import setup_task


def test_get_pythonw_path_uses_python_directory():
    with patch.object(setup_task.sys, "executable", r"C:\Python311\python.exe"):
        assert setup_task.get_pythonw_path() == r"C:\Python311\pythonw.exe"


def test_build_task_command_uses_custom_time():
    with patch.object(setup_task, "get_pythonw_path", return_value=r"C:\Python311\pythonw.exe"), patch.object(
        setup_task, "get_reminder_script_path", return_value=r"C:\project\reminder.py"
    ):
        command = setup_task.build_task_command("08:30")

    assert command[0] == "schtasks"
    assert command[command.index("/ST") + 1] == "08:30"
    assert command[-2] == r'"C:\Python311\pythonw.exe" "C:\project\reminder.py"'


def test_parse_args_reads_custom_time():
    with patch.object(setup_task.sys, "argv", ["setup_task.py", "--time", "08:30"]):
        assert setup_task.parse_args().time == "08:30"


def test_create_scheduled_task_runs_schtasks():
    with patch.object(setup_task, "build_task_command", return_value=["schtasks", "/Create"]), patch(
        "setup_task.subprocess.run"
    ) as mock_run:
        setup_task.create_scheduled_task("08:30")

    mock_run.assert_called_once_with(["schtasks", "/Create"], check=True)
