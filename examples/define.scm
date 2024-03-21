(begin
  (define n 42)
  (define x 69)
  (define l (list n x n))
  (define f (lambda (a b) (+ a (/ b 3))))
  (f
    (car l)
    (car (cdr l))))
