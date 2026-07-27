#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# Define a class for S-Expressions, and for each type of expression.

# Each VM type has three required methods: vm_type, vm_str, vm_eval
# We deliberately do not use inheritance here, in order to make it easier
# to port this code to non-OO languages.
#
# The VM Types are:
#
#	B: Boolean
#	E: not a type, but reserved for use by ESE
#	F: Function (args are pre-evaluated)
#	I: Integer
#	N: Nil
#	M: Macro (args are not pre-evaluated)
#	P: Pair
#	R: Real number (Floating point)
#	S: String
#	Y: sYmbol
#

class VMNil():

  def __init__(self):
    pass

  def vm_type(self):
    return 'N'

  def vm_str(self):
    return "()"

  def vm_eval(self, env):
    return self

class VMBoolean():

  def __init__(self, value):
    if not isinstance(value, bool):
      raise Exception('%s is not bool' % value)
    self._bool_val = ("#t" if value else "#f")

  def bool_val(self):
    return self._bool_val

  def vm_type(self):
    return 'B'

  def vm_str(self):
    return str(self._bool_val)

  def vm_eval(self, env):
    return self

class VMInteger():

  def __init__(self, value):
    if not isinstance(value, int):
      raise Exception('%s is not integer' % value)
    self._int_val = value

  def vm_type(self):
    return 'I'

  def int_val(self):
    return self._int_val

  def vm_str(self):
    return str(self._int_val)

  def vm_eval(self, env):
    return self

class VMReal():

  def __init__(self, value):
    if not isinstance(value, float):
      raise Exception('%s is not float' % value)
    self._real_val = value

  def vm_type(self):
    return 'R'

  def real_val(self):
    return self._real_val

  def vm_str(self):
    return str(self._real_val)

  def vm_eval(self, env):
    return self

class VMString():
  def __init__(self, value):
     self._str_val = str(value)

  def vm_type(self):
    return 'S'

  def str_val(self):
    return self._str_val

  def vm_str(self):
    return '"%s"' % self._str_val

  def vm_eval(self, env):
    return self

class VMSymbol():
  def __init__(self, name, sid):
    self._name = name
    self._sid = sid

  def vm_type(self):
    return 'Y'

  def name(self):
    return self._name

  def sid(self):
    return self._sid

  def vm_str(self):
    return '%s/%d' % (self._name, self._sid)

  def vm_eval(self, env):
    return env.get(self)

class VMPair():
  def __init__(self, left, right):
    self._left = left
    self._right = right

  def left(self):
    return self._left

  def right(self):
    return self._right

  def vm_type(self):
    return 'P'

  def vm_str(self):
    return "( " + self._left.vm_str() + self._tail_str()

  def _tail_str(self):
    tail = self._right
    if isinstance(tail, VMNil):
      return " )"
    if isinstance(tail, VMPair):
      return " " + tail._left.vm_str() + tail._tail_str()
    return " . " + tail.vm_str() + " )"

  def vm_eval(self, env):
    action = self._left.vm_eval(env)
    if action.vm_type() == 'M':
      args = self._right
      return action.macro()(args, env)
    if action.vm_type() == 'F':
      args = self._eval_list(self._right, env)
      return action.function()(args, env)
    raise Exception("not executable: %s" % action.vm_str())

  def _eval_list(self, tail, env):
    if tail.vm_type() == 'N':
      return tail
    if tail.vm_type() == 'P':
      return VMPair(tail.left().vm_eval(env), tail._eval_list(tail.right(), env))
    raise Exception("arg list is not a list")

class VMMacro():

  def __init__(self, macro):
    self._macro = macro

  def macro(self):
    return self._macro

  def vm_type(self):
    return 'M'

  def vm_str(self):
    return str(self._macro)

  def vm_eval(self, args, env):
    raise Exception("cannot eval a bare macro without args")

class VMFunction():

  def __init__(self, function):
    self._function = function

  def function(self):
    return self._function

  def vm_type(self):
    return 'F'

  def vm_str(self):
    return str(self._function)

  def vm_eval(self, args, env):
    raise Exception("cannot eval a bare function without args")

