#lang racket

(define (memo-proc proc)
  (let ((already-run? #f) (result #f))
    (lambda ()
      (if already-run?
          result
          (begin (set! result (proc))
                 (set! already-run? #t)
                 result)))))

(define-syntax-rule (delay exp) 
    (memo-proc (lambda () exp)))

(define-syntax-rule (cons-stream a b) 
  (cons a (delay b)))
(define-syntax-rule (force delayed-object)
  (delayed-object))

(define (stream-car stream) (car stream))
(define (stream-cdr stream) (force (cdr stream)))

(define (stream-ref s n)
  (if (= n 0)
      (stream-car s)
      (stream-ref (stream-cdr s) (- n 1))))

(define (stream-map proc s)
  (if (null? s)
      '()
      (cons-stream (proc (stream-car s))
                   (stream-map proc (stream-cdr s)))))

(define (stream-for-each proc s)
  (if (null? s)
      'done
      (begin (proc (stream-car s))
             (stream-for-each proc (stream-cdr s)))))

(define (stream-enumerate-interval low high)
  (if (> low high)
      '()
      (cons-stream
       low
       (stream-enumerate-interval (+ low 1) high))))

(define (display-line x)
  (newline)
  (display x))

(define (display-stream s)
  (stream-for-each display-line s))

(define (show x)
  (display-line x)
  x)

(define (behavior rule state)
  (cons-stream state
               (stream-map rule (behavior rule state))))
(require pict)


(define (trancelate exp)
  (if (not (pair? exp))
       exp
      (list  (cadr exp)
            (trancelate (car exp))
             (trancelate(caddr exp)))))

(define (ev exp)
  (cdr (trancelate exp)))
(define a
(trancelate '((1 - 2) + (3 + 4))))

(define (matrix-map f ma)
  (if (null? ma)
      null
      (cons (map f (car ma))
            (matrix-map  f (cdr ma)))))

(define b (list (list 1 1 1 1 1 1)
                (list 1 1 1 1 1 1)
                (list 1 1 1 1 1 1)
                (list 1 1 1 1 1 1)
                (list 1 1 1 1 1 1)
                (list 1 1 1 1 1 1)))

(define ram (lambda (x) (random 1 10)))
(define c (matrix-map ram b))

(define (listfind list a)
  (cond[(= a 1) (car list)]
       [else (listfind (cdr list) (- a 1))]))

(define (matfind mat a b)
  (listfind (listfind mat a) b))

(define (makelis n)
   (if (= n 0)
        null
       (cons n (makelis (- n 1)))))

(define (makelist n)
  (reverse (makelis n)))

(define (makeconli n b)
  (map (lambda (e) (cons n e))
       (makelist b)))

(define ten (makelist 10))
ten



(define (makemat a b)
  (let ((t (makelist a)))
    (map (lambda (x) (makeconli x b)) t)))

(define mat1 (makemat 10 10))
(define (addsound mat)
  (matrix-map (lambda (x) (cons (random 1 100) x)) mat))

(define mat2
(addsound mat1))
mat2


(define (up item mat)
  (if (< (+ (cadr item) 1 ) 11)
      (matfind mat (+ (cadr item) 1)
               (cddr item))
      null))
(define (below item mat)
  (if (> (- (cadr item) 1) 1)
  (matfind mat (- (cadr item) 1)
               (cddr item))
      null))
(define (left item mat)
  (if (> (- (cddr item) 1) 1)
  (matfind mat (cadr item)
               (- (cddr item) 1))
      null))
(define (right item mat)
  (if (< (+ (cddr item) 1) 11)
  (matfind mat (cadr item)
               (+ (cddr item) 1))
      null))

(define (sound item)
  (if (null? item)
      0
  (car item)))

(define (sumsound item mat)
  (+ (sound (up item mat))
     (sound (below item mat))
     (sound (left item mat))
     (sound (right item mat))))

(define (thex item)
  (cadr item))
(define (they item)
  (cddr item))

(define (oneside? item)
  (or (and (= (thex item) 1)
           (not (= (they item) 1)))
      (and (= (thex item) 1)
           (not (= (they item) 10)))
      (and (= (thex item) 10)
           (not (= (they item) 1)))
      (and (= (thex item) 10)
           (not (= (they item) 10)))))

(define (allsilenci? classroom)
  (< 300 (matrix-accumulate + (matrix-map sound classroom))))


  
     
(define (twoside? item)
  (or (and (= (thex item) 1)
           (= (they item) 1))
      (and (= (thex item) 1)
           (= (they item) 10))
      (and (= (thex item) 10)
           (= (they item) 1))
      (and (= (thex item) 10)
           (= (they item) 10))))



(up (matfind mat2 3 3) mat2)
(below (matfind mat2 3 3) mat2)
(left (matfind mat2 3 3) mat2)
(right (matfind mat2 3 3) mat2)

(sumsound (matfind mat2 3 3) mat2)

(define (avesound item mat)
  (cond[(oneside? item) (/ (sumsound item mat) 3)]
       [(twoside? item) (/ (sumsound item mat) 2)]
       [else (/ (sumsound item mat) 4)]))

(define (accumulate proc list)
  (if (null?  list)
      0
      (proc (car list) (accumulate proc (cdr list)))))
(define (flat list)
  (cond[(not (pair? list)) list]
       [(pair? (car list))
        (append (flat (car list))
              (flat (cdr list)))]
       [else
        (cons (car list)
              (flat (cdr list)))]))

(define (matrix-accumulate proc mat)
  (accumulate proc (flat mat)))


(oneside? (matfind mat2 3 3))

(define (avesoundx item)
  (avesound item mat2))

(matrix-map avesoundx mat2)

(matrix-map sound mat2)

(define (silence? item)
  (> 50 (avesoundx item)))

(matrix-map silence? mat2)


(define (rulemini item)
  (cond [(and (= 1 (sound item))(silence? item)) (cons 1 (cons (thex item)
                                          (they item)))]
        [(silence? item) (cons 1 (cons (thex item)
                                          (they item)))]
        [else (cons (random 1 100)
                    (cons (thex item)
                                          (they item)))]))
  (define (therule class)
    (matrix-map rulemini class))


(define (showl mat)
  (matrix-map car mat))

(define classroom
  (behavior therule mat2))

(define classroom1
  (stream-map showl classroom))

(stream-ref classroom1 1)
(stream-ref classroom1 2)
(stream-ref classroom1 3)
(stream-ref classroom1 4)
(stream-ref classroom1 5)
(stream-ref classroom1 6)
(stream-ref classroom1 7)
(stream-ref classroom1 8)
(stream-ref classroom1 9)
(stream-ref classroom1 10)
(stream-ref classroom1 11)
(stream-ref classroom1 12)
(stream-ref classroom1 13)
(stream-ref classroom1 14)
(stream-ref classroom1 15)
(stream-ref classroom1 16)
(stream-ref classroom1 17)
(stream-ref classroom1 18)
(stream-ref classroom1 19)
(stream-ref classroom1 200)


































              
  






















 
                     











