#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This class knows how to read ESE files and convert them
# to expressions.

from sys import stdin
from VMTypes import \
  VMNull, VMBoolean, VMInteger, VMReal, VMString, VMSymbol, VMPair

class Reader:

  def __init__(self, stable):
    self._symbol_table = stable

  def is_white_space(self, c):
    return c in " \t\n\r\v"

  def read_one_token(self):
    # consume any leading whitespace
    char = " "
    while char and self.is_white_space(char):
      char = stdin.read(1)
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
      char = stdin.read(1)

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
        stack.append(VMPair(left, right))
        continue
      if token == "N":
        stack.append(VMNull())
        continue

      value = self.read_one_token()
      if not value:
        raise Exception("no value")

      if token == "B":
        stack.append(VMBoolean(value == "#t"))
      if token == "I":
        stack.append(VMInteger(int(value)))
      elif token == "R":
        stack.append(VMReal(float(value)))
      elif token == "S":
        stack.append(VMString(value))
      elif token == "Y":
        sid = self._symbol_table.get(value).sid()
        stack.append(VMSymbol(value, sid))

