(define (problem newspaper) (:domain newspapers)
  (:objects
        loc-0 - loc
  loc-1 - loc
  loc-2 - loc
  paper-0 - paper
  paper-1 - paper
  paper-2 - paper
  paper-3 - paper
  paper-4 - paper
  paper-5 - paper
  paper-6 - paper
  paper-7 - paper
  paper-8 - paper
  )
  (:init 
  (at loc-0)
  (is_Home_Base loc-0)
  (unpacked paper-0)
  (unpacked paper-1)
  (unpacked paper-2)
  (unpacked paper-3)
  (unpacked paper-4)
  (unpacked paper-5)
  (unpacked paper-6)
  (unpacked paper-7)
  (unpacked paper-8)
  (wants_Paper loc-1)
  (wants_Paper loc-2)
  )
  (:goal (and
  (satisfied loc-1)
  (satisfied loc-2)))
)