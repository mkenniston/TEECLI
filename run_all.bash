#! /usr/bin/env bash

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

if ! shellcheck ./*.bash ./*/*.bash ./*/*/*.bash; then
  exit 1
fi

ALL_TARGETS=$(ls targets)
for TARGET in $ALL_TARGETS; do
  ./run_one.bash "$TARGET"
done

