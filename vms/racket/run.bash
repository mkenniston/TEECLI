#! /usr/bin/env bash

CODE=code$$.rkt
cat framework.rkt framework.ebs > $CODE
racket -t $CODE | grep "^{n: \"" | grep "\", s: \"" | grep "\"}$" | sort
rm -f $CODE

