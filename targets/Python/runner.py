#! /usr/bin/env python

# This is a skeleton program to read ESE (encoded s-expression) data
# and create the actual s-expressions.  ESE is much easier for a
# machine to read than the original human-readable s-expressions.
 
from Reader import Reader
from VM import VM
from SymbolTable import SymbolTable
from VM_Types import VM_Float
from Environment import Environment

def main():
  symbol_table = SymbolTable()
  reader = Reader(symbol_table)
  vm = VM()
  global_env = Environment()

  # FIX ME
  pi_sym = symbol_table.get("pi")
  pi_val = VM_Float(3.14159)
  global_env.set(pi_sym, pi_val)

  expr = reader.read_one_expr()
  while expr:
    vm.execute(expr, global_env)
    expr = reader.read_one_expr()

if __name__ == "__main__":
  main()

