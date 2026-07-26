#! /usr/bin/env bash

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

if ! ruff check; then
  exit 1
fi
cat tools/runtimes.ebs tools/framework.ebs \
    | racket -t tools/compiler.rkt \
    | targets/Python/runner.py

