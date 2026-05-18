# setup_task.py
import argparse
import os
import subprocess
import sys
from pathlib import Path


TASK_NAME = "DianwaimaiReminder"
DEFAULT_TASK_TIME = "11:10"


def get_pythonw_path():
    base_dir = os.path.dirname(sys.executable)
    return os.path.join(base_dir, "pythonw.exe")


def get_reminder_script_path():
    return str(Path(__file__).resolve().with_name("reminder.py"))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", default=DEFAULT_TASK_TIME)
    return parser.parse_args()


def build_task_command(task_time):
    pythonw_path = get_pythonw_path()
    script_path = get_reminder_script_path()
    return [
        "schtasks",
        "/Create",
        "/TN",
        TASK_NAME,
        "/SC",
        "DAILY",
        "/ST",
        task_time,
        "/TR",
        f'"{pythonw_path}" "{script_path}"',
        "/F",
    ]


def create_scheduled_task(task_time):
    subprocess.run(build_task_command(task_time), check=True)


def main():
    args = parse_args()
    create_scheduled_task(args.time)


if __name__ == "__main__":
    main()
