#! /usr/bin/env python

# Define a class for S-Expressions, and for each type of expression.

class Expression:

  def expr_type(self):
    raise Exception('expr_type() must be overridden')

  def expr_str(self):
    raise Exception('expr_str() must be overridden')

  def expr_eval(self, env):
    raise Exception('expr_eval() must be overridden')

class Pair(Expression):

  def __init__(self, left, right):
    self._left = left
    self._right = right

  def expr_type(self):
    return 'P'

  def expr_str(self):
    return "( " + self._left.expr_str() + self._tail_str()

  def _tail_str(self):
    tail = self._right
    if isinstance(tail, AtomNil):
      return " )"
    if isinstance(tail, Pair):
      return " " + tail._left.expr_str() + tail._tail_str()
    return " . " + tail.expr_str() + " )"

  def expr_eval(self, env):
    return self  # FIX ME

class Atom(Expression):
  def __init__(self):
    Expression.__init__(self)

class AtomNil(Atom):

  def __init__(self):
    Atom.__init__(self)

  def expr_type(self):
    return 'N'

  def expr_str(self):
    return "()"

  def expr_eval(self, env):
    return self

class AtomInt(Atom):

  def __init__(self, value):
    Atom.__init__(self)
    if not isinstance(value, int):
      raise Exception('%s is not integer' % value)
    self._int_val = value

  def expr_type(self):
    return 'I'

  def int_val(self):
    return self._int_val

  def expr_str(self):
    return str(self._int_val)

  def expr_eval(self, env):
    return self

class AtomFloat(Atom):

  def __init__(self, value):
    Atom.__init__(self)
    if not isinstance(value, float):
      raise Exception('%s is not float' % value)
    self._float_val = value

  def expr_type(self):
    return 'F'

  def float_val(self):
    return self._float_val

  def expr_str(self):
    return str(self._float_val)

  def expr_eval(self, env):
    return self

class AtomStr(Atom):
  def __init__(self, value):
     Atom.__init__(self)
     self._str_val = str(value)

  def expr_type(self):
    return 'S'

  def str_val(self):
    return self._str_val

  def expr_str(self):
    return '"%s"' % self._str_val

  def expr_eval(self, env):
    return self

class AtomSym(Atom):
  def __init__(self, name, sid):
    Atom.__init__(self)
    self._name = name
    self._sid = sid

  def expr_type(self):
    return 'Y'

  def name(self):
    return self._name

  def sid(self):
    return self._sid

  def expr_str(self):
    return '%s/%d' % (self._name, self._sid)

  def expr_eval(self, env):
    return env.get(self)

