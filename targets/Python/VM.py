#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# Execute an S-Expression.

class VM:

  def execute(self, expr, env):
    print(expr.vm_eval(env).vm_str())

