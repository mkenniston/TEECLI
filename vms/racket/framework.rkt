
#lang racket 
(define vm-name "python")

(define expect "expect")

(define current-group-prefix (make-parameter vm-name))

(define-syntax-rule (test-group name expr ...)
  (parameterize ([current-group-prefix (string-append (current-group-prefix) "/" name)])
    expr ...))

(define (passed-test-line name)
  (string-append "{n: \"" name "\", s: \"pass\"}"))

(define (failed-test-line name expected actual)
  (string-append "{n: \"" name "\", s: \"fail\", e: \"" (~v expected) "\", a: \"" (~v actual) "\"}"))

(define-syntax-rule (run-test name expr expect-str expected)
  (let ((actual expr)
        (test-name (string-append (current-group-prefix) "/" name)))
    (if (string=? expect-str "expect") (void)
      (raise "syntax error, run-test didn't find \"expect\""))
    (if (= actual expected)
      (displayln (passed-test-line test-name))
      (displayln (failed-test-line test-name expected actual))
    )
  )
)

