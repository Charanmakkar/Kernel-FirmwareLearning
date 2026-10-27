# M01 reference solution and reasoning

Use strtol with errno, end-pointer, range and trailing-character checks. Check argc before reading argv[1]. Build with warnings enabled and test 0, a negative value and a mixed value such as 12x. Capture the failing return code. A reproducibility note names compiler version and source commit. A shell transcript without source and build flags is incomplete.
