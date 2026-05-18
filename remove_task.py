# remove_task.py
import subprocess


TASK_NAME = "DianwaimaiReminder"


def build_remove_task_command():
    return ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"]


def remove_scheduled_task():
    subprocess.run(build_remove_task_command(), check=True)


if __name__ == "__main__":
    remove_scheduled_task()
