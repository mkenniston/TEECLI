#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This function populates all the built-in functions and values.

from VMTypes import \
  VMPair, VMBoolean, VMInteger, VMReal, VMString, VMSymbol, \
  VMMacro, VMFunction
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

    # The properties of define, set!, and let:
    # (define variable value)
    #   - if the variable exists in the environment chain, set that one
    #   - else create the variable in the current environment, and set it
    # (set! variable value)
    #   - if the variable exists in the environment chain, set that one
    #   - else raise an exception
    # (let ((variable value) ...) ...)
    #   - create a new environment, create the variable in that
    #     environment, and set its value

    env.set(symbol_table.get("define"), VMMacro(bi_define))
    env.set(symbol_table.get("set!"), VMMacro(bi_set_bang))

    env.set(symbol_table.get("vm-type"), VMFunction(bi_vm_type))
    env.set(symbol_table.get("quote"), VMMacro(bi_quote))
    env.set(symbol_table.get("length"), VMFunction(bi_length))

    env.set(symbol_table.get("cons"), VMFunction(bi_cons))
    env.set(symbol_table.get("car"), VMFunction(bi_car))
    env.set(symbol_table.get("cdr"), VMFunction(bi_cdr))
    env.set(symbol_table.get("list"), VMFunction(bi_list))

    # ARITHMETIC OPS

    env.set(symbol_table.get("+"), VMFunction(bi_plus))
    env.set(symbol_table.get("-"), VMFunction(bi_minus))
    env.set(symbol_table.get("*"), VMFunction(bi_times))

    # MISC

# internal utility functions

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

def num_items(args):
  len = 0
  while args.vm_type() != 'N':
    if args.vm_type() != 'P':
      raise Exception("cannot find length of non-list")
    len += 1
    args = args.right()
  return len

def as_num(obj):
  if obj.vm_type() == 'I':
    return obj.int_val()
  if obj.vm_type() == 'R':
    return obj.real_val()
  raise Exception("%s is not a number" % obj.env_str())

# actual builtin implementations

def bi_vm_type(args, env):
  require_exact_arg_number(1, num_items(args))
  arg1 = args.left()
  return VMString(arg1.vm_type())

def bi_quote(args, env):
  require_exact_arg_number(1, num_items(args))
  arg1 = args.left()
  return arg1

def bi_length(args, env):
  require_exact_arg_number(1, num_items(args))
  arg1 = args.left()
  return VMInteger(num_items(arg1))

def bi_cons(args, env):
  require_exact_arg_number(2, num_items(args))
  arg1 = args.left()
  arg2 = args.right().left()
  return VMPair(arg1, arg2)

def bi_car(args, env):
  require_exact_arg_number(1, num_items(args))
  arg1 = args.left()
  require_type(arg1, VMPair)
  return arg1.left()

def bi_cdr(args, env):
  require_exact_arg_number(1, num_items(args))
  arg1 = args.left()
  require_type(arg1, VMPair)
  return arg1.right()

def bi_list(args, env):
  return args

def bi_define(args, env):
    # (define variable value)
    #   - if the variable exists in the environment chain, set that one
    #   - else create the variable in the current environment, and set it
  require_type(env, Environment)
  require_exact_arg_number(2, num_items(args))
  arg1 = args.left()
  arg2 = args.right().left()
  sym = arg1
  val = arg2.vm_eval(env)
  require_type(sym, VMSymbol)
  env = env.find_env(sym.sid()) or env
  env.set(sym, val)
  return val

def bi_set_bang(args, env):
    # (set! variable value)
    #   - if the variable exists in the environment chain, set that one
    #   - else raise an exception
  require_type(env, Environment)
  require_exact_arg_number(2, num_items(args))
  arg1 = args.left()
  arg2 = args.right().left()
  sym = arg1
  val = arg2.vm_eval(env)
  require_type(sym, VMSymbol)
  env = env.find_env(sym.sid())
  if env is None:
    raise Exception("set! requires an existing variable")
  env.set(sym, val)
  return val

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

