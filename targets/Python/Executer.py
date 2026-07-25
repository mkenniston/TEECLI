#! /usr/bin/env python

from Environment import Environment

# Execute an S-Expression.

class Executer:

  def execute(self, expr):
    global_env = Environment()
    print(expr.__eval__(global_env))

