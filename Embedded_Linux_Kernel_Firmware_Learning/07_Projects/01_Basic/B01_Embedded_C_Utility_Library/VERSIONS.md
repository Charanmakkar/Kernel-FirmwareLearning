# B01 versions

Source contract: ISO C11 with CHAR_BIT=8, uint8_t/uint16_t/uint32_t and size_t. Host-independent logic; x86-64 Windows is the only initially observed execution host. Python runner requires Python 3.9+; executed host version recorded in evidence. Observed compiler: LLVM-MinGW Clang 22.1.0-rc3, target x86_64-w64-windows-gnu, toolchain path recorded in JSON. GCC coverage, Linux execution, emulator and MCU execution remain separate pending checks unless later evidence is added.

No kernel, linker script, board wiring, peripheral or external package dependency applies. include/, src/, tests/, scripts/, docs/, exercises/ and evidence/ are present. config/ and hardware/ are omitted because B01 has neither OS configuration nor physical hardware. build/ is generated output and excluded from the distributable ZIP.
