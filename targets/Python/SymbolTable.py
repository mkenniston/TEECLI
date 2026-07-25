#! /usr/bin/env python

# Implement a Symbol Table, which contains only the name and sid of
# each symbol.

from VM_Types import VM_Sym

class SymbolTable:

  def __init__(self):
    self._next_id = 0
    self._table = {}

  def get(self, name):
    if name not in self._table:
      self._table[name] = VM_Sym(name, self._next_id)
      self._next_id += 1
    return self._table[name]
