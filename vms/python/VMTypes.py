#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# Define a class for S-Expressions, and for each type of expression.

# Each VM type has three required methods: vm_type, vm_str, vm_eval
# We deliberately do not use inheritance here, in order to make it easier
# to port this code to non-OO languages.
#

class VMVoid():

  _type = None

  def __init__(self):
    pass

  def vm_type(self):
    return VMVoid._type

  def vm_str(self):
    return "#<void>"

  def vm_eval(self, env):
    return self

class VMNull():

  _type = None

  def __init__(self):
    pass

  def vm_type(self):
    return VMNull._type

  def vm_str(self):
    return "()"

  def vm_eval(self, env):
    return self

class VMBoolean():

  _type = None

  def __init__(self, value):
    if not isinstance(value, bool):
      raise Exception('%s is not a bool' % value)
    self._bool_val = value

  def bool_val(self):
    return self._bool_val

  def vm_type(self):
    return VMBoolean._type

  def vm_str(self):
    if self._bool_val:
      return "#t"
    return "#f"

  def vm_eval(self, env):
    return self

class VMInteger():

  _type = None

  def __init__(self, value):
    if not isinstance(value, int):
      raise Exception('%s is not an integer' % value)
    self._int_val = value

  def vm_type(self):
    return VMInteger._type 

  def int_val(self):
    return self._int_val

  def vm_str(self):
    return str(self._int_val)

  def vm_eval(self, env):
    return self

class VMReal():

  _type = None

  def __init__(self, value):
    if not isinstance(value, float):
      raise Exception('%s is not a float' % value)
    self._real_val = value

  def vm_type(self):
    return VMReal._type

  def real_val(self):
    return self._real_val

  def vm_str(self):
    return str(self._real_val)

  def vm_eval(self, env):
    return self

class VMString():

  _type = None

  def __init__(self, value):
    if not isinstance(value, str):
      raise Exception('%s is not a string' % value)
    self._str_val = str(value)

  def vm_type(self):
    return VMString._type

  def str_val(self):
    return self._str_val

  def vm_str(self):
    return '"%s"' % self._str_val

  def vm_eval(self, env):
    return self

class VMSymbol():

  _type = None

  def __init__(self, name, sid):
    if not isinstance(name, str):
      raise Exception('%s is not a string' % name)
    if not isinstance(sid, int):
      raise Exception('%s is not an integer' % sid)
    self._name = name
    self._sid = sid

  def vm_type(self):
    return VMSymbol._type

  def name(self):
    return self._name

  def sid(self):
    return self._sid

  def vm_str(self):
    return '%s/%d' % (self._name, self._sid)

  def vm_eval(self, env):
    return env.get(self)

class VMPair():

  _type = None

  def __init__(self, left, right):
    self._left = left
    self._right = right

  def left(self):
    return self._left

  def right(self):
    return self._right

  def vm_type(self):
    return VMPair._type

  def vm_str(self):
    return "( " + self._left.vm_str() + self._tail_str()

  def _tail_str(self):
    tail = self._right
    if tail.vm_type() == VMNull._type:
      return " )"
    if tail.vm_type() == VMPair._type:
      return " " + tail._left.vm_str() + tail._tail_str()
    return " . " + tail.vm_str() + " )"

  def vm_eval(self, env):
    action = self._left.vm_eval(env)
    if action.vm_type() == VMMacro._type:
      args = self._right
      return action.macro()(args, env)
    if action.vm_type() == VMFunction._type:
      args = self._eval_list(self._right, env)
      return action.function()(args, env)
    raise Exception("not executable: %s" % action.vm_str())

  def _eval_list(self, tail, env):
    if tail.vm_type() == VMNull._type:
      return tail
    if tail.vm_type() == VMPair._type:
      return VMPair(tail.left().vm_eval(env), tail._eval_list(tail.right(), env))
    raise Exception("arg list is not a list")

class VMMacro():

  _type = None

  def __init__(self, macro):
    self._macro = macro

  def macro(self):
    return self._macro

  def vm_type(self):
    return VMMacro._type

  def vm_str(self):
    return str(self._macro)

  def vm_eval(self, args, env):
    raise Exception("cannot eval a bare macro without args")

class VMFunction():

  _type = None

  def __init__(self, function):
    self._function = function

  def function(self):
    return self._function

  def vm_type(self):
    return VMFunction._type

  def vm_str(self):
    return str(self._function)

  def vm_eval(self, args, env):
    raise Exception("cannot eval a bare function without args")

