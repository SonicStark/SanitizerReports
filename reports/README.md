# Sanitizer Report Samples

These samples are located at `data`. Actually they are raw text printed into *stdout* when running all available test cases about sanitizers from [*LLVM 16.0.0 Release*](https://github.com/llvm/llvm-project/releases/tag/llvmorg-16.0.0). So naturally, they have a structure similar to the `llvm-project/compiler-rt/test` directory for easier view and comparison.

The LLVM suite is built on *Ubuntu 20.04.4 LTS x86_64* platform.

`scripts/analyse.py` is the script used for extracting text output of test cases from *llvm-lit* reports.
