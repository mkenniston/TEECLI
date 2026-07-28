#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This function populates all the built-in functions and values.

from VMTypes import \
  VMBoolean, VMInteger, VMReal, VMString, VMSymbol, VMMacro, VMFunction
from Environment import Environment

class BuiltIns:

  def populate(self, symbol_table, env):

    # BOOLEAN CONSTANTS

    true_val = VMBoolean(True)
    env.set(symbol_table.get("#t"), true_val)
    env.set(symbol_table.get("True"), true_val)

    false_val = VMBoolean(False)
    env.set(symbol_table.get("#f"), false_val)
    env.set(symbol_table.get("False"), false_val)

    # BASIC OPS

    env.set(symbol_table.get("vm-type"), VMFunction(bi_vm_type))
    env.set(symbol_table.get("set!"), VMMacro(bi_set_bang))
    env.set(symbol_table.get("quote"), VMMacro(bi_quote))
    env.set(symbol_table.get("length"), VMFunction(bi_length))

    # ARITHMETIC OPS

    env.set(symbol_table.get("+"), VMFunction(bi_plus))
    env.set(symbol_table.get("-"), VMFunction(bi_minus))
    env.set(symbol_table.get("*"), VMFunction(bi_times))

    # MISC

def require_exact_arg_number(expected, actual):
  if actual != expected:
    raise Exception("%d args found where %d expected" %
      (actual, expected))

def require_min_arg_number(expected, actual):
  if actual < expected:
    raise Exception("%d args found where at least %d expected" %
      (actual, expected))

def require_type(obj, type):
  if not isinstance(obj, type):
    raise Exception("%s is not of type %s" % (obj.vm_str(), type))

def bi_vm_type(args, env):
  require_exact_arg_number(1, num_items(args))
  return VMString(args.left().vm_type())

def bi_quote(args, env):
  require_exact_arg_number(1, num_items(args))
  return args.left()

def bi_length(args, env):
  require_exact_arg_number(1, num_items(args))
  return VMInteger(num_items(args.left()))

def num_items(args):
  len = 0
  while args.vm_type() != 'N':
    if args.vm_type() != 'P':
      raise Exception("cannot find length of non-list")
    len += 1
    args = args.right()
  return len

def bi_set_bang(args, env):
  require_type(env, Environment)
  require_exact_arg_number(2, num_items(args))
  sym = args.left()
  val = args.right().left().vm_eval(env)
  require_type(sym, VMSymbol)
  env.set(sym, val)
  return val

def as_num(obj):
  if obj.vm_type() == 'I':
    return obj.int_val()
  if obj.vm_type() == 'R':
    return obj.real_val()
  raise Exception("%s is not a number" % obj.env_str())

def bi_plus(args, env):
  require_type(env, Environment)
  sum = 0
  is_float = False
  while args.vm_type() != 'N':
    val = args.left()
    sum += as_num(val)
    if val.vm_type() == 'F':
      is_float = True
    args = args.right()
  return VMReal(sum) if is_float else VMInteger(sum)

def bi_minus(args, env):
  require_type(env, Environment)
  require_min_arg_number(1, num_items(args))
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
  return VMReal(sum) if is_float else VMInteger(sum)

def bi_times(args, env):
  require_type(env, Environment)
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
  return VMReal(product) if is_float else VMInteger(product)

