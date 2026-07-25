#! /usr/bin/env python

# This class knows how to read ESE files and convert them
# to expressions.

import sys
from Expressions import AtomNil, AtomInt, AtomFloat, AtomStr, AtomSym, Pair

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
        stack.append(Pair(left, right))
        continue
      if token == "N":
        stack.append(AtomNil())
        continue

      value = self.read_one_token()
      if not value:
        raise Exception("no value")

      if token == "I":
        stack.append(AtomInt(int(value)))
      elif token == "F":
        stack.append(AtomFloat(float(value)))
      elif token == "S":
        stack.append(AtomStr(value))
      elif token == "Y":
        sid = self._symbol_table.get(value).sid()
        stack.append(AtomSym(value, sid))

