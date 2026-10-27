# M14 reference solution and reasoning

Place reproducible source/configuration in the external tree or own layer. Install with explicit modes and directories, include the resulting package in the image, and declare the correct init integration. Keep factory defaults under immutable image control and device settings on a separately defined writable path. On first boot create settings atomically only when absent; do not overwrite an existing user configuration on each service start.
