#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This class knows how to read ESE files and convert them
# to expressions.

import sys
from VMTypes import VM_Nil, VM_Bool, VM_Int, VM_Real, VM_Str, VM_Sym, VM_Pair

class Reader:

  def __init__(self, stable):
    self._symbol_table = stable

  def is_white_space(self, c):
    return c in " \t\n\r\v"

  def read_one_token(self):
    # consume any leading whitespace
    char = " "
    while char and self.is_white_space(char):
      char = sys.stdin.read(1)
    # read one string of non-whitespace (unless quoted with \\)
    quoting = False
    token = ""
    while True:
      if not char:
        # hit EOF
        if token == "":
          return None
        return token
      if not quoting and char == "\\":
        quoting = True
      elif not quoting and self.is_white_space(char):
        return token
      else:
        token += char
        quoting = False
      char = sys.stdin.read(1)

  def read_one_expr(self):
    stack = []
    while True:
      token = self.read_one_token()
      if not token:
        if len(stack) == 0:
          return None
        raise Exception("premature EOF")
      if token == "E":
        if len(stack) != 1:
          raise Exception("not a valid end")
        return stack.pop()

      if token == "P":
        if len(stack) < 2:
          raise Exception("no pair to push")
        right = stack.pop()
        left = stack.pop()
        stack.append(VM_Pair(left, right))
        continue
      if token == "N":
        stack.append(VM_Nil())
        continue

      value = self.read_one_token()
      if not value:
        raise Exception("no value")

      if token == "B":
        stack.append(VM_Bool(value == "#t"))
      if token == "I":
        stack.append(VM_Int(int(value)))
      elif token == "R":
        stack.append(VM_Real(float(value)))
      elif token == "S":
        stack.append(VM_Str(value))
      elif token == "Y":
        sid = self._symbol_table.get(value).sid()
        stack.append(VM_Sym(value, sid))

