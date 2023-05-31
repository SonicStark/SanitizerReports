# SanitizerReports

## Introduction

*SanitizerReports* aims to help you grab various reports from sanitizers when running their unit tests and regression tests,
by patching
*lit* ([LLVM Integrated Tester](https://llvm.org/docs/CommandGuide/lit.html))
and
*FileCheck*([Flexible pattern matching file verifier](https://llvm.org/docs/CommandGuide/FileCheck.html)).

We also provide some report texts as examples. See `./reports` for more details.

*SanitizerReports* is under the Apache License v2.0 with LLVM Exceptions (same as [llvm/llvm-project](https://github.com/llvm/llvm-project)).
See `LICENSE` for more details.

## Tutorial

We are going to take
[LLVM 16.0.0 Release](https://github.com/llvm/llvm-project/releases/tag/llvmorg-16.0.0)
working on *Ubuntu 20.04.4 LTS (x86_64)* as an example.
The same method is also applicable to other versions of *llvm-project* and other OS.

### Check Requirements

See https://releases.llvm.org/16.0.0/docs/GettingStarted.html#requirements .

### Get the Source Code

Download the whole source tree from 
https://github.com/llvm/llvm-project/releases/tag/llvmorg-16.0.0 .

Remember we need source code of all related subprojects like *Clang*, so download
https://github.com/llvm/llvm-project/releases/download/llvmorg-16.0.0/llvm-project-16.0.0.src.tar.xz .

You can extract the source code with
```shell
tar -xf llvm-project-16.0.0.src.tar.xz
```
after downloaded. Then you will get a directory *llvm-project-16.0.0.src*.

### Configure LLVM

This may sound confusing, but it's the fact - we actually need to start all building stuffs 
from `llvm-project-16.0.0.src/llvm`.

```shell
cd llvm-project-16.0.0.src;

mkdir mybuild myinstall;

cd mybuild;

cmake -G "Unix Makefiles" \
    -DLLVM_ENABLE_PROJECTS="compiler-rt;clang" \
    -DLLVM_INCLUDE_TESTS=ON \
    -DLLVM_TARGETS_TO_BUILD="X86" \
    -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_INSTALL_PREFIX="`pwd`/../myinstall" \
    -DCMAKE_C_COMPILER="/usr/bin/gcc" \
    -DCMAKE_CXX_COMPILER="/usr/bin/g++" \
    "`pwd`/../llvm";
```

Here we enable both *compiler-rt* and *clang*, which is necessary for running the test cases.
See https://releases.llvm.org/16.0.0/docs/GettingStarted.html#local-llvm-configuration for more details.

### Build LLVM

Assuming that we are still in `llvm-project-16.0.0.src/mybuild`, run

```shell
make -j$(nproc)
```

and wait for all things get done.

### Apply Patches

If it has built successfully, let's go to `llvm-project-16.0.0.src/mybuild/bin` for this step.

#### Patch *FileCheck*

Make a backup of `llvm-project-16.0.0.src/mybuild/bin/FileCheck` before patching:
```shell
cp FileCheck FileCheck.bak
```

Then replace it with our pythonic version, i.e. `SanitizerReports/llvm-FileCheck/FileCheck`.

And check if it works well:
```shell
echo "HelloWorld!" | ./FileCheck
```

#### Patch *llvm-lit*

`llvm-project-16.0.0.src/mybuild/bin/llvm-lit` is actually a python script, just like our pythonic `FileCheck`.

You can open and view it as plain text:
```shell
cat llvm-lit
```

Here I get:
```python
#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import os
import sys

config_map = {}

def map_config(source_dir, site_config):
    global config_map
    source_dir = os.path.realpath(source_dir)
    source_dir = os.path.normcase(source_dir)
    site_config = os.path.normpath(site_config)
    config_map[source_dir] = site_config

# Set up some builtin parameters, so that by default the LLVM test suite
# configuration file knows how to find the object tree.
builtin_parameters = { 'build_mode' : '.' }

# Allow generated file to be relocatable.
from pathlib import Path
def path(p):
    if not p: return ''
    return str((Path(__file__).parent / p).resolve())


map_config(path(r'../../compiler-rt/test/tsan/lit.cfg.py'), path(r'../projects/compiler-rt/test/tsan/X86_64Config/lit.site.cfg.py'))
map_config(path(r'../../compiler-rt/test/tsan/lit.cfg.py'), path(r'../projects/compiler-rt/test/tsan/X86_64LinuxDynamicConfig/lit.site.cfg.py'))
map_config(path(r'../../clang/test/lit.cfg.py'), path(r'../tools/clang/test/lit.site.cfg.py'))
map_config(path(r'../../clang/test/Unit/lit.cfg.py'), path(r'../tools/clang/test/Unit/lit.site.cfg.py'))
map_config(path(r'../../llvm/utils/lit/tests/lit.cfg'), path(r'../utils/lit/lit.site.cfg'))
map_config(path(r'../../llvm/test/lit.cfg.py'), path(r'../test/lit.site.cfg.py'))
map_config(path(r'../../llvm/test/Unit/lit.cfg.py'), path(r'../test/Unit/lit.site.cfg.py'))

builtin_parameters['config_map'] = config_map

# Make sure we can find the lit package.
llvm_source_root = path(r'../../llvm')
sys.path.insert(0, os.path.join(llvm_source_root, 'utils', 'lit'))

if __name__=='__main__':
    from lit.main import main
    main(builtin_parameters)
```

It indicates that the true body of `lit` is located at `llvm-project-16.0.0.src/llvm/utils/lit/lit`.

Go there and locate `llvm-project-16.0.0.src/llvm/utils/lit/lit/cl_arguments.py`.
Now open and edit this file, modified it like what 
https://github.com/SonicStark/SanitizerReports/blob/6156709ab2ca3b82064928d660baad0b38c4cfdd/llvm-lit/lit/cl_arguments.py#L239-L249
does, i.e., let *llvm-lit* receive file path from environment variable `LIT_JSON_OUTPUT` as an alternative to `--output` option.
Because when running the testcases it's diffcult to 
change the behavior of *llvm-lit* by passing command line options.

### Run Testcases

Let's check what testcases is needed by us. 
Back to `llvm-project-16.0.0.src/mybuild` and run
```shell
make help | grep 'check-' | less
```
and it will show you all regression tests and unit tests we can run.
As for sanitizers, I have screened out the needed ones:
 * check-lsan
 * check-ubsan
 * check-asan-dynamic
 * check-asan
 * check-dfsan
 * check-msan
 * check-hwasan-lam
 * check-hwasan
 * check-tsan-dynamic
 * check-tsan
 * check-ubsan-minimal
 * check-gwp_asan

Now we run `check-ubsan-minimal` as an example:
```shell
LIT_JSON_OUTPUT="`pwd`/ubsan_min.json" make check-ubsan-minimal
```

### Access Report

After the last step done, you will get `llvm-project-16.0.0.src/mybuild/ubsan_min.json.pid`.
It's a JSON file which contains fields like:
```text
{
  "__version__": [
    ...,
    ...,
    ...
  ],
  "elapsed": ...,
  "tests": [
    {
      "code":   "...",
      "elapsed": ...,
      "name":   "...",
      "output": "..."
    },
    {
      ...
    },
    ...
  ]
}
```

Then you can find content of the report printed by the sanitizer tested before in `output` key.

### Parse Report

Text in `output` key may contain those stuffs not printed by santizer, error messages, or even multiple reports.
So additional text processing is usually necessary to get precise content of the report.

## Links

 - [LLVM Testing Infrastructure Guide](https://llvm.org/docs/TestingGuide.html#llvm-testing-infrastructure-guide)
 - [test-suite Guide](https://llvm.org/docs/TestSuiteGuide.html)
 - [lit - LLVM Integrated Tester](https://llvm.org/docs/CommandGuide/lit.html#lit-llvm-integrated-tester)
 - [FileCheck - Flexible pattern matching file verifier](https://llvm.org/docs/CommandGuide/FileCheck.html)
