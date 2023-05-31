# lit - A Software Testing Tool

## About

*lit* is a portable tool for executing LLVM and Clang style test suites,
summarizing their results, and providing indication of failures.
This is a modified version of *lit* based on
[LLVM 16.0.4 Release](https://github.com/llvm/llvm-project/releases/tag/llvmorg-16.0.4).

The key changes are located at *lit/cl_arguments.py* - we need to receive file path
from environment variable `LIT_JSON_OUTPUT` as an alternative to `--output` option,
since
```shell
make check LIT_ARGS="--output /to/path"
```
doesn't seem to work.

Other changes are:
 - A better example *ManyTests*.
 - Some comments about where the so-called *output* comes from.
 - Rename the entrance *lit.py* to *llvm-lit* for easier usage.
 - Drop some cumbersome files.


## Documentation

The official *lit* documentation is available online at the LLVM
Command Guide: http://llvm.org/cmds/lit.html.


## Source

The *lit* source is available as part of LLVM, in the LLVM source repository:
https://github.com/llvm/llvm-project/tree/main/llvm/utils/lit
