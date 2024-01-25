# Eupnea-ChromeOS kernel

This repo has been merged into https://github.com/eupnea-project/linux-kernels

<details>
<summary>View the old readme</summary>

# Eupnea-ChromeOS kernel

[Kernel docs page](https://eupnea-linux.github.io/docs/project/kernels#chromeos-eupnea-kernel)

# Building the Eupnea-ChromeOS kernel

[Build instructions](https://eupnea-linux.github.io/docs/compile/kernel#building-the-eupnea-chromeos-kernel)

# Overlaid configs

To allow continuously importing changes from the upstream kernel
config ([currently arch linux](https://raw.githubusercontent.com/archlinux/svntogit-packages/packages/linux/trunk/config))
all changes made by the Eupnea team are stored as individual overlay configs that are appended to the base config.

A daily workflow pulls the fresh upstream config into base-kernel.conf , appends the overlay configs (from
kernel-conf-overlays) and runs `make olddefconfig` to automatically combine the configs (the appended config options are
prioritized over the base config options) to create combined-kernel.conf which can then used to build the kernel.

[Overlays-readme](kernel-conf-overlays/README.md)
