#! /usr/bin/env python

# Define a class for S-Expressions, and for each type of expression.

# Each VM type has three required methods: vm_type, vm_str, vm_eval
# We deliberately do not use inheritance here, in order to make it easier
# to port this code to non-OO languages.

class VM_Pair():
  def __init__(self, left, right):
    self._left = left
    self._right = right

  def vm_type(self):
    return 'P'

  def vm_str(self):
    return "( " + self._left.vm_str() + self._tail_str()

  def _tail_str(self):
    tail = self._right
    if isinstance(tail, VM_Nil):
      return " )"
    if isinstance(tail, VM_Pair):
      return " " + tail._left.vm_str() + tail._tail_str()
    return " . " + tail.vm_str() + " )"

  def vm_eval(self, env):
    return self  # FIX ME

class VM_Nil():

  def __init__(self):
    pass

  def vm_type(self):
    return 'N'

  def vm_str(self):
    return "()"

  def vm_eval(self, env):
    return self

class VM_Int():

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

class VM_Float():

  def __init__(self, value):
    if not isinstance(value, float):
      raise Exception('%s is not float' % value)
    self._float_val = value

  def vm_type(self):
    return 'F'

  def float_val(self):
    return self._float_val

  def vm_str(self):
    return str(self._float_val)

  def vm_eval(self, env):
    return self

class VM_Str():
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

class VM_Sym():
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

