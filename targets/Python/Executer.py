#! /usr/bin/env python

# Execute an S-Expression.

class Executer:

  def execute(self, expr, env):
    print(expr.expr_eval(env).expr_str())

