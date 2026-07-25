#! /usr/bin/env python

# Environments match values with variables (symobls), using lexical scoping.

class Environment:

  def __init__(self, parent=None):
    self._parent = parent
    self._values = {}

  def create(self, symbol):
    if symbol.sid() in self._values:
      raise Exception("attempt to double-declare local %s" % symbol.__str__())
    self._values[symbol.sid()] = None

  def get_val(self, symbol):
    if symbol.sid() in self._values:
      return self._values[symbol.sid()]
    if self._parent is None:
      raise Exception("uncreated symbol %s" % symbol.__str__())
    val = self._parent.get_val(symbol)
    if val is None:
      raise Exception("unbound symbol %s" % symbol.__str__())
    return val

  def set_val(self, symbol, value):
    if symbol.sid() in self._values:
      self._values[symbol.sid()] = value
      return value
    if self._parent is None:
      raise Exception("uncreated symbol %s" % symbol.__str__())
    self.set_val(symbol, value)

