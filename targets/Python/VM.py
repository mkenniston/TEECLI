#! /usr/bin/env python

# Execute an S-Expression.

class VM:

  def execute(self, expr, env):
    print(expr.vm_eval(env).vm_str())

