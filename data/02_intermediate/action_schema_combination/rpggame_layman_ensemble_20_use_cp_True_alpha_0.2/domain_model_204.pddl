(define (domain rpggame)
    (:requirements :negative-preconditions :strips :typing)
    (:types cells swords)
    (:predicates (arm-free) (at-hero ?loc - cells)  (at-sword ?s - swords ?loc - cells)  (connected ?from - cells ?to - cells)  (has-monster ?loc - cells)  (has-trap ?loc - cells)  (holding ?s - swords)  (is-destroyed ?obj)  (trap-disarmed ?loc))
    (:action destroy-sword
        :parameters (?s - swords ?loc - cells)
        :precondition (and (at-hero ?loc) (at-sword ?s ?loc) (holding ?s))
        :effect (and (not (holding ?s)) (is-destroyed ?s) (arm-free))
    )
     (:action disarm-trap
        :parameters (?loc - cells)
        :precondition (and (at-hero ?loc) (has-trap ?loc) (arm-free))
        :effect (and (not (has-trap ?loc)) (trap-disarmed ?loc))
    )
     (:action move
        :parameters (?from - cells ?to - cells)
        :precondition (and (at-hero ?from) (connected ?from ?to) (not (has-trap ?from)) (not (is-destroyed ?to)) (not (has-monster ?to)) (not (has-trap ?to)))
        :effect (and (not (at-hero ?from)) (at-hero ?to) (is-destroyed ?from))
    )
     (:action move-to-monster
        :parameters (?loc-from - cells ?loc-to - cells)
        :precondition (and (at-hero ?loc-from) (connected ?loc-from ?loc-to) (has-monster ?loc-to))
        :effect (and (not (at-hero ?loc-from)) (at-hero ?loc-to))
    )
     (:action move-to-trap
        :parameters (?current - cells ?trap - cells)
        :precondition (and (at-hero ?current) (connected ?current ?trap) (has-trap ?trap))
        :effect (and (not (at-hero ?current)) (at-hero ?trap))
    )
     (:action pick-sword
        :parameters (?s - swords ?loc - cells)
        :precondition (and (at-hero ?loc) (at-sword ?s ?loc) (arm-free))
        :effect (and (not (at-sword ?s ?loc)) (holding ?s) (not (arm-free)))
    )
)