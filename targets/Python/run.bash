#! /usr/bin/env bash

if ! ruff check; then
  exit 1
fi
cat tools/runtimes.ebs tools/framework.ebs \
    | racket -t tools/compiler.rkt \
    | targets/Python/runner.py

