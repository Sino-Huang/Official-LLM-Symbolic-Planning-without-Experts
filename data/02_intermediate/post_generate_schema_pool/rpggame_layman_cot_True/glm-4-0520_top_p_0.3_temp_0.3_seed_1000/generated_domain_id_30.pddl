(define (domain rpggame)

    (:requirements :strips :typing :negative-preconditions)

    (:types
    swords cells
)

    (:predicates
        (at-hero ?loc - cells) ;;  Hero's cell location
        (at-sword ?s - swords ?loc - cells) ;; Sword cell location
        (has-monster ?loc - cells) ;; Indicates if a cell location has a monster
        (has-trap ?loc - cells) ;; Indicates if a cell location has a trap
        (is-destroyed ?obj) ;; Indicates if a chell or sword has been destroyed
        (connected ?from ?to - cells) ;; connects cells
        (arm-free) ;; Hero's hand is free
        (holding ?s - swords) ;; Hero's holding a sword
        (trap-disarmed ?loc) ;; It becomes true when a trap is disarmed
    )

    (:action move-to-monster
        :parameters (?from - cells ?to - cells)
        :precondition (and
            (at-hero ?from)
            (connected ?from ?to)
            (has-monster ?to)
        )
        :effect (and
            (not (at-hero ?from))
            (at-hero ?to)
        )
    )
    (:action disarm-trap
        :parameters (?loc - cells)
        :precondition (and
            (at-hero ?loc)
            (has-trap ?loc)
            (arm-free)
        )
        :effect (and
            (trap-disarmed ?loc)
        )
    )
    (:action pick-sword
        :parameters (?s - swords ?loc - cells)
        :precondition (and
            (at-hero ?loc)
            (at-sword ?s ?loc)
            (arm-free)
        )
        :effect (and
            (not (arm-free))
            (not (at-sword ?s ?loc))
            (holding ?s)
        )
    )
    (:action move-to-trap
        :parameters (?from - cells ?to - cells)
        :precondition (and
            (at-hero ?from)
            (connected ?from ?to)
            (has-trap ?to)
        )
        :effect (and
            (not (at-hero ?from))
            (at-hero ?to)
        )
    )
    (:action destroy-sword
        :parameters (?s - swords)
        :precondition (holding ?s)
        :effect (and
            (not (holding ?s))
            (is-destroyed ?s)
            (arm-free)
        )
    )
    (:action move
        :parameters (?from - cells ?to - cells)
        :precondition (and
            (at-hero ?from)
            (connected ?from ?to)
            (not (has-trap ?from))
            (not (has-trap ?to))
            (not (has-monster ?to))
            (not (is-destroyed ?to))
        )
        :effect (and
            (not (at-hero ?from))
            (at-hero ?to)
            (is-destroyed ?from)
        )
    )
)