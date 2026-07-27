#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This is a skeleton program to read ESE (encoded s-expression) data
# and create the actual s-expressions.  ESE is much easier for a
# machine to read than the original human-readable s-expressions.
 
from Reader import Reader
from SymbolTable import SymbolTable
from Environment import Environment
from BuiltIns import BuiltIns

class VirtualMachine:

  def __init__(self):
    self._symbol_table = SymbolTable()
    self._reader = Reader(self._symbol_table)
    self._global_env = Environment()
    BuiltIns().populate(self._symbol_table, self._global_env)

  def read_one_expr(self):
    return self._reader.read_one_expr()

  def execute(self, expr):
    print(expr.vm_eval(self._global_env).vm_str())

def main():
  vm = VirtualMachine()
  expr = vm.read_one_expr()
  while expr:
    vm.execute(expr)
    expr = vm.read_one_expr()

if __name__ == "__main__":
  main()

