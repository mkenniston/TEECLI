#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This function populates all the built-in functions and values.

from VMTypes import VM_Bool, VM_Int, VM_Real, VM_Macro, VM_Function
from Environment import Environment

class BuiltIns:

  def populate(self, symbol_table, env):

    # BOOLEAN CONSTANTS

    true_val = VM_Bool(True)
    env.set(symbol_table.get("#t"), true_val)
    env.set(symbol_table.get("True"), true_val)

    false_val = VM_Bool(False)
    env.set(symbol_table.get("#f"), false_val)
    env.set(symbol_table.get("False"), false_val)

    # BASIC OPS

    env.set(symbol_table.get("set!"), VM_Macro(vm_set_bang))
    env.set(symbol_table.get("quote"), VM_Macro(vm_quote))
    env.set(symbol_table.get("length"), VM_Function(vm_length))

    # ARITHMETIC OPERATORS

    env.set(symbol_table.get("pi"), VM_Real(3.1415926))
    env.set(symbol_table.get("+"), VM_Function(vm_plus))
    env.set(symbol_table.get("-"), VM_Function(vm_minus))
    env.set(symbol_table.get("*"), VM_Function(vm_times))

    # MISC

def vm_quote(args, env):
  len = num_items(args)
  if len != 1:
    raise Exception("%d args found where 1 expected" % len)
  return args.left()

def vm_length(args, env):
  len = num_items(args)
  if len != 1:
    raise Exception("%d args found where 1 expected" % len)
  return VM_Int(num_items(args.left()))

def num_items(args):
  len = 0
  while args.vm_type() != 'N':
    if args.vm_type() != 'P':
      raise Exception("cannot find length of non-list")
    len += 1
    args = args.right()
  return len

def vm_set_bang(args, env):
  if not isinstance(env, Environment):
    raise Exception("%s is not an Environment" % env.vm_str())
  len = num_items(args)
  if len != 2:
    raise Exception("%d args found where 2 expected" % len)
  sym = args.left()
  val = args.right().left().vm_eval(env)
  if sym.vm_type() != 'Y':
    raise Exception("%s is not a symbol" % sym.vm_str())
  env.set(sym, val)
  return val

def as_num(obj):
  if obj.vm_type() == 'I':
    return obj.int_val()
  if obj.vm_type() == 'R':
    return obj.real_val()
  raise Exception("%s is not a number" % obj.env_str())

def vm_plus(args, env):
  if not isinstance(env, Environment):
    raise Exception("%s is not an Environment" % env.vm_str())
  sum = 0
  is_float = False
  while args.vm_type() != 'N':
    val = args.left()
    sum += as_num(val)
    if val.vm_type() == 'F':
      is_float = True
    args = args.right()
  return VM_Real(sum) if is_float else VM_Int(sum)

def vm_minus(args, env):
  if not isinstance(env, Environment):
    raise Exception("%s is not an Environment" % env.vm_str())
  len = num_items(args)
  if len < 1:
    raise Exception("%d args found where at least 1 expected" % len)
  is_float = False
  val = args.left()
  sum = as_num(val)
  if val.vm_type() == 'F':
    is_float = True
  args = args.right()
  while args.vm_type() != 'N':
    val = args.left()
    sum -= as_num(val)
    if val.vm_type() == 'F':
      is_float = True
    args = args.right()
  return VM_Real(sum) if is_float else VM_Int(sum)

def vm_times(args, env):
  if not isinstance(env, Environment):
    raise Exception("%s is not an Environment" % env.vm_str())
  product = 1
  is_float = False
  while args.vm_type() != 'N':
    val = args.left()
    if val.vm_type() == 'I':
      product *= val.int_val()
    elif val.vm_type() == 'F':
      product *= val.float_val()
      is_float = True
    else:
      raise("%s is not a number in '*'" % val.vm_str())
    args = args.right()
  return VM_Real(product) if is_float else VM_Int(product)

