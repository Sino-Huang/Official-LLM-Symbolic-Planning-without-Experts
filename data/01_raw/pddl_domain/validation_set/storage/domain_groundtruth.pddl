; IPC5 Domain: Storage Propositional
; Authors: Alfonso Gerevini and Alessandro Saetti 

(define (domain storage)
       (:requirements :typing :strips)
       (:types
              hoist surface place - object
              container depot - place
              store_area transit_area - area
              area crate - surface
       )

       (:predicates
              (clear ?s - store_area)
              (crate_in ?c - crate ?p - place)
              (store_area_in ?s - store_area ?p - place)
              (available ?h - hoist)
              (lifting ?h - hoist ?c - crate)
              (at ?h - hoist ?a - area)
              (on ?c - crate ?s - store_area)
              (connected ?a1 ?a2 - area)
              (compatible ?c1 ?c2 - crate)
       )

       (:action lift
              :parameters (?h - hoist ?c - crate ?a1 - store_area ?a2 - area ?p - place)
              :precondition (and (connected ?a1 ?a2) (at ?h ?a2) (available ?h)
                     (on ?c ?a1) (store_area_in ?a1 ?p))
              :effect (and (not (on ?c ?a1)) (clear ?a1)
                     (not (available ?h)) (lifting ?h ?c) (not (crate_in ?c ?p)))
       )

       (:action drop
              :parameters (?h - hoist ?c - crate ?a1 - store_area ?a2 - area ?p - place)
              :precondition (and (connected ?a1 ?a2) (at ?h ?a2) (lifting ?h ?c)
                     (clear ?a1) (store_area_in ?a1 ?p))
              :effect (and (not (lifting ?h ?c)) (available ?h)
                     (not (clear ?a1)) (on ?c ?a1) (crate_in ?c ?p))
       )

       (:action move
              :parameters (?h - hoist ?from ?to - store_area)
              :precondition (and (at ?h ?from) (clear ?to) (connected ?from ?to))
              :effect (and (not (at ?h ?from)) (at ?h ?to) (not (clear ?to)) (clear ?from))
       )

       (:action go-out
              :parameters (?h - hoist ?from - store_area ?to - transit_area)
              :precondition (and (at ?h ?from) (connected ?from ?to))
              :effect (and (not (at ?h ?from)) (at ?h ?to) (clear ?from))
       )

       (:action go-in
              :parameters (?h - hoist ?from - transit_area ?to - store_area)
              :precondition (and (at ?h ?from) (connected ?from ?to) (clear ?to))
              :effect (and (not (at ?h ?from)) (at ?h ?to) (not (clear ?to)))
       )
)