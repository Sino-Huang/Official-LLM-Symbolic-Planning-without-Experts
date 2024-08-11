(define (domain rpggame)
    (:requirements :negative-preconditions :strips :typing)
    (:types cells swords)
    (:predicates (arm-free) (at-hero ?loc - cells)  (at-sword ?s - swords ?loc - cells)  (connected ?from - cells ?to - cells)  (has-monster ?loc - cells)  (has-trap ?loc - cells)  (holding ?s - swords)  (is-destroyed ?obj)  (trap-disarmed ?loc))
    (:action destroy-sword
        :parameters (?s - swords ?loc - cells)
        :precondition (and (holding ?s) (at-hero ?loc))
        :effect (and (not (holding ?s)) (is-destroyed ?s) (when (has-trap ?loc) (is-destroyed ?loc)) (when (has-monster ?loc) (is-destroyed ?loc)))
    )
     (:action disarm-trap
        :parameters (?loc - cells)
        :precondition (and (at-hero ?loc) (has-trap ?loc) (arm-free))
        :effect (and (trap-disarmed ?loc))
    )
     (:action move
        :parameters (?from - cells ?to - cells)
        :precondition (and (at-hero ?from) (connected ?from ?to) (not (is-destroyed ?to)))
        :effect (and (not (at-hero ?from)) (at-hero ?to) (is-destroyed ?from))
    )
     (:action move-to-monster
        :parameters (?from - cells ?loc - cells)
        :precondition (and (at-hero ?from) (connected ?from ?loc) (has-monster ?loc) (not (is-destroyed ?loc)))
        :effect (and (not (at-hero ?from)) (at-hero ?loc))
    )
     (:action move-to-trap
        :parameters (?loc - cells ?next-loc - cells)
        :precondition (and (at-hero ?loc) (connected ?loc ?next-loc) (not (is-destroyed ?next-loc)) (has-trap ?next-loc))
        :effect (and (not (at-hero ?loc)) (at-hero ?next-loc))
    )
     (:action pick-sword
        :parameters (?s - swords ?loc - cells)
        :precondition (and (at-hero ?loc) (at-sword ?s ?loc) (arm-free))
        :effect (and (not (at-sword ?s ?loc)) (holding ?s) (not (arm-free)))
    )
)