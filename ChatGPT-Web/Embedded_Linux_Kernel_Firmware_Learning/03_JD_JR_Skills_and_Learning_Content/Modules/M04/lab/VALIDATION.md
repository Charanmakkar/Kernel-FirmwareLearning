# Validation

On 27 October 2026, make test compiled fd_owner.cpp with g++ 13.3.0, C++17, warnings as errors and executed all ownership assertions. Output: fd_owner: move, release, scope cleanup, invalid owner passed. This verifies the stated small Linux host example, not every possible close error.
