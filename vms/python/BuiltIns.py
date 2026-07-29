#! /usr/bin/env python

# TEECLI - Test Execution Environment for Cross-Language Implementations
# Copyright (c) 2026 Michael S. Kenniston
# Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

# This function populates all the built-in functions and values.

from VMTypes import \
  VMVoid, VMNull, VMBoolean, VMInteger, VMReal, VMString, VMSymbol, \
  VMPair, VMMacro, VMFunction
from Environment import Environment

vm_void = None
vm_null = None
vm_boolean = None
vm_integer = None
vm_real = None
vm_string = None
vm_symbol = None
vm_pair = None
vm_macro = None
vm_function = None

class BuiltIns:

  def populate(self, symbol_table, env):

    # FUNDAMENTAL TYPES

    global vm_void, vm_null, vm_boolean, vm_integer, vm_real, \
      vm_string, vm_symbol, vm_pair, vm_macro, vm_function

    vm_void = symbol_table.get("vm-void")
    VMVoid._type = env.set(vm_void, vm_void)
    vm_null = symbol_table.get("vm-null")
    VMNull._type = env.set(vm_null, vm_null)
    vm_boolean = symbol_table.get("vm-boolean")
    VMBoolean._type = env.set(vm_boolean, vm_boolean)
    vm_integer = symbol_table.get("vm-integer")
    VMInteger._type = env.set(vm_integer, vm_integer)
    vm_real = symbol_table.get("vm-real")
    VMReal._type = env.set(vm_real, vm_real)
    vm_string = symbol_table.get("vm-string")
    VMString._type = env.set(vm_string, vm_string)
    vm_symbol = symbol_table.get("vm-symbol")
    VMSymbol._type = env.set(vm_symbol, vm_symbol)
    vm_pair = symbol_table.get("vm-pair")
    VMPair._type = env.set(vm_pair, vm_pair)
    vm_macro = symbol_table.get("vm-macro")
    VMMacro._type = env.set(vm_macro, vm_macro)
    vm_function = symbol_table.get("vm-function")
    VMFunction._type = env.set(vm_function, vm_function)

    # CONSTANTS

    null = VMNull()
    env.set(symbol_table.get("null"), null)
    env.set(symbol_table.get("empty"),null)
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

    env.set(symbol_table.get("vm-type"), VMFunction(bi_vm_type))
    env.set(symbol_table.get("quote"), VMMacro(bi_quote))
    env.set(symbol_table.get("length"), VMFunction(bi_length))
    env.set(symbol_table.get("cons"), VMFunction(bi_cons))
    env.set(symbol_table.get("car"), VMFunction(bi_car))
    env.set(symbol_table.get("cdr"), VMFunction(bi_cdr))
    env.set(symbol_table.get("list"), VMFunction(bi_list))
    env.set(symbol_table.get("if"), VMMacro(bi_if))
    env.set(symbol_table.get("cond"), VMMacro(bi_cond))
    env.set(symbol_table.get("define"), VMMacro(bi_define))
    env.set(symbol_table.get("set!"), VMMacro(bi_set_bang))
    env.set(symbol_table.get("eval"), VMFunction(bi_eval))
    env.set(symbol_table.get("let"), VMMacro(bi_let))
    env.set(symbol_table.get("let*"), VMMacro(bi_let_star))

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
  while args.vm_type() != vm_null:
    if args.vm_type() != vm_pair:
      raise Exception("cannot find length of non-list")
    len += 1
    args = args.right()
  return len

def as_num(obj):
  if obj.vm_type() == vm_integer:
    return obj.int_val()
  if obj.vm_type() == vm_real:
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

def bi_if(args, env):
  require_exact_arg_number(3, num_items(args))
  arg1 = args.left()
  arg2 = args.right().left()
  arg3 = args.right().right().left()
  condition = arg1.vm_eval(env)
  require_type(condition, VMBoolean)
  if condition.bool_val():
    return arg2.vm_eval(env)
  return arg3.vm_eval(env)

def bi_cond(args, env):
  while args.vm_type() != vm_null:
    require_type(args, VMPair)
    clause = args.left()
    require_exact_arg_number(2, num_items(clause))
    condition = clause.left()
    if condition.vm_type() == vm_symbol and condition.name() == "else":
      condition = True
    else:
      condition = condition.vm_eval(env)
      require_type(condition, VMBoolean)
      condition = condition.bool_val()
    if condition:
      return clause.right().left().vm_eval(env)
    args = args.right()
  return vm_void

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
  return vm_void

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
  return vm_void

def bi_eval(args, env):
  require_exact_arg_number(1, num_items(args))
  arg1 = args.left()
  return arg1.vm_eval(env)

def both_lets(args, env, use_old):
  require_min_arg_number(2, num_items(args))
  new_env = Environment(env)
  base_env = env if use_old else new_env
  all_bindings = args.left()
  args = args.right()
  while all_bindings.vm_type() != vm_null:
    require_type(all_bindings, VMPair)
    binding = all_bindings.left()
    require_exact_arg_number(2, num_items(binding))
    var = binding.left()
    val = binding.right().left().vm_eval(base_env)
    new_env.set(var, val)
    all_bindings = all_bindings.right()
  result = vm_void
  while args.vm_type() != vm_null:
    require_type(args, VMPair)
    expr = args.left()
    result = expr.vm_eval(new_env)
    args = args.right()
  return result

def bi_let(args, env):
  return both_lets(args, env, True)

def bi_let_star(args, env):
  return both_lets(args, env, False)

def bi_plus(args, env):
  require_type(env, Environment)
  sum = 0
  is_float = False
  while args.vm_type() != vm_null:
    val = args.left()
    sum += as_num(val)
    if val.vm_type() == vm_real:
      is_float = True
    args = args.right()
  return VMReal(sum) if is_float else VMInteger(sum)

def bi_minus(args, env):
  require_type(env, Environment)
  require_min_arg_number(1, num_items(args))
  is_float = False
  val = args.left()
  sum = as_num(val)
  if val.vm_type() == vm_real:
    is_float = True
  args = args.right()
  while args.vm_type() != vm_null:
    val = args.left()
    sum -= as_num(val)
    if val.vm_type() == vm_real:
      is_float = True
    args = args.right()
  return VMReal(sum) if is_float else VMInteger(sum)

def bi_times(args, env):
  require_type(env, Environment)
  product = 1
  is_float = False
  while args.vm_type() != vm_null:
    val = args.left()
    if val.vm_type() == vm_integer:
      product *= val.int_val()
    elif val.vm_type() == vm_real:
      product *= val.float_val()
      is_float = True
    else:
      raise("%s is not a number in '*'" % val.vm_str())
    args = args.right()
  return VMReal(product) if is_float else VMInteger(product)

