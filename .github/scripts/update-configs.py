#!/usr/bin/env python3
import os
import subprocess
from urllib.request import urlretrieve


def bash(command: str) -> str:
    output = subprocess.check_output(command, shell=True, text=True).strip()
    print(output, flush=True)
    return output


if __name__ == "__main__":
    # pull fresh arch linux config to use as base.conf
    urlretrieve(url="https://raw.githubusercontent.com/archlinux/svntogit-packages/packages/linux/trunk/config",
                filename="base.conf")

    # duplicate base.conf to temp_combined.conf
    with open("base.conf", "r") as base:
        with open("temp_combined.conf", "w") as combined:
            combined.write(base.read())

    # append all overlays to combined.conf
    for file in os.listdir("kernel-conf-overlays"):
        if file != "README.md":
            with open(f"kernel-conf-overlays/{file}", "r") as overlay:
                with open("temp_combined.conf", "a") as combined:
                    combined.write("\n" + overlay.read())

    # init chromeos kernel git repo
    bash("git init kernel")
    os.chdir("./kernel")
    bash("git remote add origin https://chromium.googlesource.com/chromiumos/third_party/kernel")
    stable_branches = []
    for branch in bash("git ls-remote origin 'refs/heads/*'").split("\t"):
        branch = branch.split("\n")[0]
        if branch.startswith("refs/heads/release-R") and branch.endswith(".B-chromeos-5.10"):
            stable_branches.append(branch.split("/")[2])

    # sort by release number
    stable_branches.sort(key=lambda x: int(x.split("-")[1][1:]))
    # get the latest branch
    latest_version = stable_branches[-1]

    # clone latest branch
    bash(f"git pull --depth=1 origin {latest_version}")

    # Copy config into fresh chromeos kernel repo
    bash("cp ../temp_combined.conf ./.config")

    # Update config
    bash("make olddefconfig")

    # Copy new config back to eupnea repo
    bash("cp ./.config ../combined-kernel.conf")

    # Update build script
    with open("../kernel_build.py", "r") as file:
        build_script = file.readlines()
    build_script[11] = f'branch_name = "{latest_version}"\n'
    with open("../kernel_build.py", "w") as file:
        file.writelines(build_script)
