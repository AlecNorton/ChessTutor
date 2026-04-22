python3 - <<'PY' > chess_tutor_deps.repos
import os
import subprocess

folders = [
    "arm_control",
    "cmake_modules",
    "dynamixel_sdk",
    "dynamixel_sdk_custom_interfaces",
    "dynamixel_sdk_examples",
    "dynamixel_workbench",
    "dynamixel_workbench_toolbox",
    "open_manipulator",
    "open_manipulator_msgs",
    "open_manipulator_x_controller",
    "open_manipulator_x_description",
    "open_manipulator_x_libs",
    "rbe500-example",
    "rbe500_example_py",
    "robotis_manipulator",
]

print("repositories:")
for folder in folders:
    if not os.path.isdir(folder):
        continue
    git_dir = os.path.join(folder, ".git")
    if not os.path.exists(git_dir):
        continue

    def run(cmd):
        return subprocess.check_output(cmd, cwd=folder, text=True).strip()

    try:
        url = run(["git", "remote", "get-url", "origin"])
    except Exception:
        url = ""

    try:
        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    except Exception:
        branch = "main"

    print(f"  {folder}:")
    print(f"    type: git")
    print(f"    url: {url}")
    print(f"    version: {branch}")
PY