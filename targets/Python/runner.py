#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This is a skeleton program to read ESE (encoded s-expression) data
# and create the actual s-expressions.  ESE is much easier for a
# machine to read than the original human-readable s-expressions.
 
from Reader import Reader
from VM import VM
from SymbolTable import SymbolTable
from Environment import Environment
from BuiltIns import BuiltIns

def main():
  symbol_table = SymbolTable()
  reader = Reader(symbol_table)
  vm = VM()
  global_env = Environment()
  BuiltIns().populate(symbol_table, global_env)

  expr = reader.read_one_expr()
  while expr:
    vm.execute(expr, global_env)
    expr = reader.read_one_expr()

if __name__ == "__main__":
  main()

