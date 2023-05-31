# FileCheck - Flexible pattern matching file verifier


## About

*FileCheck* is originally designed to read two files
(one from standard input, and one specified on the command line)
and uses one to verify the other.
What's more, the file to verify is read from standard input
unless the `--input-file` option is used.

However, it hinders our exploration of sanitizer's report - it suppresses
the content of input file unless we use `--dump-input` option.

Here we provide you with a dummy *FileCheck*, which does nothing but redirects
input file into stdout as text. It is written in Python, and uses *Shebang*
```shell
#!/usr/bin/env python3
```
to masquerade as the original *FileCheck*. You may need to modify the *Shebang*
to fit your os environment.

One more thing, make sure you have set the proper *execute* permission for
this *FileCheck* after replacing the original one.


## Documentation

The official *FileCheck* documentation is available online at the LLVM
Command Guide: https://llvm.org/docs/CommandGuide/FileCheck.html.


## Source

The *FileCheck* source is available as part of LLVM,
in the LLVM source repository:
https://github.com/llvm/llvm-project/tree/main/llvm/utils/FileCheck
