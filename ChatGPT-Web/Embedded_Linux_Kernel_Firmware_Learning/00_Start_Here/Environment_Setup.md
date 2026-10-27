# Development environment and version policy

## Host path

Use a disposable x86_64 Linux virtual machine for kernel experiments. Ubuntu 24.04 LTS is the general user-space teaching host; use an Ubuntu 22.04 LTS VM for the frozen Yocto 5.0.9 exercise because that release's supported-host list includes 22.04. Windows users can start C and POSIX exercises in WSL2, but the kernel you are modifying or loading a module into must be the intended disposable guest. A container shares its host kernel and is not an independent kernel test machine. [YOCTO-HOST]

For the general path, a planning allocation of 4 CPU cores, 8 GB RAM and 30 GB free space is comfortable for the small host projects. For image builds, prefer 8 CPU cores, 16 to 32 GB RAM and 150 to 250 GB free SSD space; these are planning estimates, not measured requirements. Yocto 5.0.9 documents 90 GB disk and 8 GB RAM for a representative `core-image-sato` build, with more useful for caches and complex images. Check the selected release before provisioning. [YOCTO-HOST]

These commands describe a learner-owned Ubuntu VM. They were not all executed in the authoring environment. Review package installation in your own VM:

```sh
sudo apt update
sudo apt install build-essential git ripgrep gdb gdb-multiarch gdbserver strace file binutils \
  make cmake pkg-config python3 python3-venv socat unzip xz-utils \
  gcc-aarch64-linux-gnu qemu-user qemu-system-arm qemu-system-x86 \
  bc bison flex libssl-dev libelf-dev libncurses-dev device-tree-compiler
gcc --version
python3 --version
uname -a
```

Use the specific extra host-package list in I01 and I04 for their image builds. Create a dedicated writable work directory with no spaces, keep source and build outputs separate, and retain `.config`, source tags and command lines. Do not run ordinary compilation as root. Never run a kernel module built for one kernel against a different kernel's headers or release just to see if it loads.

## Version contract

| Component | Teaching baseline | Meaning |
| --- | --- | --- |
| C | C11 source, GCC 13.3 host checks where available | Portable core code with explicit POSIX extensions |
| C++ | C++17 ownership examples | Optional deeper C++ depends on the JD |
| Linux drivers | Upstream v6.12 source API | Frozen teaching target; not a claim that 6.12.0 is current or patched |
| Buildroot | 2025.02.1 | Frozen full-system QEMU exercise; use its generated kernel contract |
| Yocto | 5.0.9 Scarthgap | Frozen qemux86-64 layer exercise on documented host |
| FreeRTOS | Kernel V11.1.0 POSIX port | Actual RTOS task/queue code on host; MCU timings pending |
| QEMU | Record installed version and machine type | Linux user mode and full-system emulation are distinct |

The exact per-project `VERSIONS.md` takes precedence where a BSP needs a different kernel. An installed host compiler version is observed evidence; the named learner baseline is a target configuration. Keep those columns separate. Before connecting a product to a network or deploying it, move the frozen examples to a maintained release, review API differences and rerun acceptance tests. Do not silently substitute a new release and retain old validation claims.

## What emulation establishes

QEMU Linux user mode runs a foreign-architecture application and translates system calls using the host kernel. It does not boot the target Linux kernel. Full-system QEMU boots a guest kernel and devices in the machine model; a generic `virt` machine is not a Raspberry Pi electrical model. A host protocol test proves framing logic for its tested cases; it does not prove line voltage, real UART DMA, cable noise tolerance or interrupt latency. [QEMU-USER] [QEMU-VIRT]

## Hardware route when you reach it

Use Raspberry Pi 4 Model B for the optional Linux GPIO/I2C exercises and a NUCLEO-F446RE for MCU learning. The project-specific hardware notes are authoritative for wiring. Read board revision markings, jumper states, connector labels and peripheral voltage requirements before connecting. A USB-to-UART adapter must expose compatible logic levels; RS-232 line levels are a different interface. A logic analyzer is useful for framing and timing; an oscilloscope is needed for electrical waveforms. No purchase is needed for B01 through B04 or the host capstone simulations. [PI-HW] [NUCLEO]

Keep power disconnected while changing connections. The first physical robot demonstration should use a low-energy bench setup with motors lifted, current limits and a separate reachable means to remove actuator power. Scaling to an industrial robot requires separate electrical, mechanical and functional-safety engineering beyond this learning package.
