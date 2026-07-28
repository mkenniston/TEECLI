#! /usr/bin/env racket

; TEECLI - Test Execution Environment for Cross-Language Implementations
; Copyright (c) 2026 Michael S. Kenniston
; Open-source licensed under LGPL 2.1.  See the LICENSE file for details.

#lang racket

(define (escape-whitespace str)
  (regexp-replace*
    #px"\\s|\\\\" 
    (if (symbol? str) (symbol->string str) str)
    "\\\\\\0"))

(define (display-ese expr)
  (cond
    [(null? expr) (display " N")]
    [(string? expr) (display " S ") (display (escape-whitespace expr))]
    [(symbol? expr) (display " Y ") (display (escape-whitespace expr))]
    [(exact-integer? expr) (display " I ") (display expr)]
    [(flonum? expr) (display " R ") (display expr)]
    [(boolean? expr) (display " B ") (display expr)]
    [(pair? expr) (display-ese (car expr))
                   (display-ese (cdr expr))
                   (display " P")]
    [else (raise-user-error "bad expr")]
  ))

(for ([expr (in-producer read eof)])
  (display-ese expr)
  (display " E\n"))
(display "\n")
