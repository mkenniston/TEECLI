#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# Implement a Symbol Table, which contains only the name and sid of
# each symbol.

from VMTypes import VM_Sym

class SymbolTable:

  def __init__(self):
    self._next_id = 0
    self._table = {}

  def get(self, name):
    if name not in self._table:
      self._table[name] = VM_Sym(name, self._next_id)
      self._next_id += 1
    return self._table[name]
