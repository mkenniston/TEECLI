#! /usr/bin/env bash

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

if [ -z "$TEECLI_DIR" ]; then
  echo "\$TEECLI_DIR is not defined"
  exit 1
fi

if [ ! -r "$TEECLI_DIR" ]; then
  echo "$TEECLI_DIR is not a readable directory"
  exit 2
fi

if ! ruff check; then
  exit 3
fi

TOOLS="$TEECLI_DIR"/tools
VM="$TEECLI_DIR"/vms/python
cat "$TOOLS"/runtimes.ebs \
    "$TOOLS"/framework.ebs \
    "$VM"/python_specific.ebs \
    | racket -t "$TOOLS"/compiler.rkt \
    | "$VM"/VirtualMachine.py

