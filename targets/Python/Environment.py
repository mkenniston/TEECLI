#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.
# Environments match values with variables (symbols), using lexical scoping.

class Environment:

  def __init__(self, parent=None):
    self._parent = parent
    self._values = {}

  def _find_env(self, sid):
    if sid in self._values:
      return self
    if self._parent is None:
      return None
    return self._parent._find_env(sid)

  def set(self, symbol, value):
    sid = symbol.sid()
    env = self._find_env(sid) or self
    env._values[sid] = value
    return value

  def get(self, symbol):
    sid = symbol.sid()
    env = self._find_env(sid)
    if env is None:
      raise Exception("%s: undefined" % symbol.vm_str())
    return self._values[sid]

