# M04 Build systems linking and C++ ownership

## Objectives and prerequisites

Prerequisites: M02.

Inspect ELF objects, diagnose link/runtime mismatches and use a small RAII wrapper without copying an owning resource.

## Lesson


Preprocessing expands includes and macros; compilation produces assembly; assembly produces object files; linking chooses definitions and assigns final locations. Use `gcc -E`, `gcc -S`, `gcc -c`, `nm`, `readelf` and `objdump` to see the stages. A declaration permits a reference; a definition supplies storage or executable code. Multiple definitions, missing definitions and an incompatible calling convention are different problems.

The application binary interface defines details such as argument passing, register usage, data layout and symbol conventions. A C function called from C++ may need `extern "C"` linkage. A library built for another CPU, incompatible floating-point ABI or libc environment is not repaired by adding an include directory. Inspect the architecture, interpreter and required symbols. A sysroot groups target headers and libraries for cross compilation; it is distinct from the host compiler's own runtime. [CMAKE]

A linker script places sections into memory regions. Bare-metal firmware needs addresses that agree with the chip's flash/RAM map, startup copy/zero code and vector placement. An initialized variable can have a load image in flash and a runtime address in RAM. `.bss` usually consumes runtime zero-initialized storage without storing all those zero bytes in the load image. Read the map file to establish memory usage; binary file size alone is not the RAM footprint. [LD]

In C++, resource acquisition is initialization, or RAII, ties cleanup to object lifetime. An owning file-descriptor wrapper closes in its destructor and disables accidental copying; moving transfers ownership and invalidates the old owner. A borrowed integer descriptor is not an owner. Keep destructor behavior nonthrowing and define whether a close failure can be reported separately. `std::unique_ptr` expresses exclusive memory ownership; shared ownership can hide cycles and unclear shutdown. Optional C++ depth includes templates, standard containers and exception policy when required by the JD. [CPP]

Make is adequate for a small C reference project. CMake describes targets and usage requirements, while Yocto/Buildroot assemble systems and dependencies at another level. They solve different scopes. Include compiler flags with the target, keep tests callable, and verify one clean build to detect undeclared dependencies. Reproducibility additionally needs pinned inputs, timestamps/tool behavior, paths and controlled external downloads.


## Worked lab and expected behavior


Run `readelf -h` and `nm` on B01's `build/test_util` executable and B05's resulting executable. To inspect a separate object, compile a source file with `gcc -c` and inspect the resulting `.o`. Inspect a host executable's interpreter with `readelf -l`. Compare an undefined reference at link time with a missing shared library at runtime. For C++, attempt the independent exercise first, then run `make test` in this module's `lab` directory to compile and execute `fd_owner.cpp`. Acceptance is that each successful open has one owner and one close, including early error paths.

Troubleshoot by stage: a missing header is a compile search-path problem; an undefined reference requires the intended definition/library and correct linkage; `Exec format error` requires target/loader inspection. Do not randomly add library flags until a build happens to pass.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain static versus dynamic linking, ABI versus API, and unique versus shared ownership. Interview bank: linking, C++ and cross-platform errors.

## Mastery checklist

- Diagnose a failure by build stage.
- Inspect ELF architecture and symbols.
- Explain LMA versus VMA in a firmware image.
- Demonstrate one resource owner through a move.

## Primary references

[LD] GNU ld linker scripts. [CMAKE] CMake 3.28 toolchain manual. [CPP] C++ Core Guidelines. [CLOSE] Linux close semantics.
