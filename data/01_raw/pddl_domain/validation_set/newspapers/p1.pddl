(define (problem newspaper) (:domain newspapers)
  (:objects
        loc-0 - loc
  loc-1 - loc
  loc-2 - loc
  loc-3 - loc
  paper-0 - paper
  paper-1 - paper
  paper-2 - paper
  paper-3 - paper
  paper-4 - paper
  )
  (:init 
  (at loc-0)
  (is_Home_Base loc-0)
  (unpacked paper-0)
  (unpacked paper-1)
  (unpacked paper-2)
  (unpacked paper-3)
  (unpacked paper-4)
  (wants_Paper loc-1)
  (wants_Paper loc-2)
  (wants_Paper loc-3)
  )
  (:goal (and
  (satisfied loc-1)
  (satisfied loc-2)
  (satisfied loc-3)))
)