(define (domain rpggame)
    (:requirements :negative-preconditions :strips :typing)
    (:types cells swords)
    (:predicates (arm-free) (at-hero ?loc - cells)  (at-sword ?s - swords ?loc - cells)  (connected ?from - cells ?to - cells)  (has-monster ?loc - cells)  (has-trap ?loc - cells)  (holding ?s - swords)  (is-destroyed ?obj)  (trap-disarmed ?loc))
    (:action destroy-sword
        :parameters (?s - swords)
        :precondition (holding ?s)
        :effect (and (not (holding ?s)) (is-destroyed ?s))
    )
     (:action disarm-trap
        :parameters (?loc - cells)
        :precondition (and (at-hero ?loc) (has-trap ?loc) (arm-free))
        :effect (and (not (has-trap ?loc)) (trap-disarmed ?loc))
    )
     (:action move
        :parameters (?from - cells ?to - cells)
        :precondition (and (at-hero ?from) (connected ?from ?to) (not (is-destroyed ?to)))
        :effect (and (not (at-hero ?from)) (at-hero ?to) (is-destroyed ?from))
    )
     (:action move-to-monster
        :parameters (?from - cells ?to - cells)
        :precondition (and (at-hero ?from) (has-monster ?to) (not (is-destroyed ?to)) (connected ?from ?to))
        :effect (and (not (at-hero ?from)) (at-hero ?to))
    )
     (:action move-to-trap
        :parameters (?from - cells ?to - cells)
        :precondition (and (at-hero ?from) (has-trap ?to) (connected ?from ?to) (not (is-destroyed ?to)))
        :effect (and (not (at-hero ?from)) (at-hero ?to))
    )
     (:action pick-sword
        :parameters (?s - swords ?loc - cells)
        :precondition (and (at-hero ?loc) (at-sword ?s ?loc) (arm-free))
        :effect (and (not (at-sword ?s ?loc)) (holding ?s) (not (arm-free)))
    )
)