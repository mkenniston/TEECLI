#! /usr/bin/env bash

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

if [ $# -ne 1 ]; then
  echo "usage: $0 <vm>"
  exit 1
fi

VM=$1
echo "running: $VM"
./vms/"$VM"/run_"$VM".bash

