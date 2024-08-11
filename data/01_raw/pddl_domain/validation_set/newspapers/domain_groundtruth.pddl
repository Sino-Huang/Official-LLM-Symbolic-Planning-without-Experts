(define (domain newspapers)
    (:requirements :strips :typing)
    (:types
        loc paper
    )
    (:predicates
        (at ?loc - loc)
        (is_Home_Base ?loc - loc)
        (satisfied ?loc - loc)
        (wants_Paper ?loc - loc)
        (unpacked ?paper - paper)
        (carrying ?paper - paper)
    )

    (:action pick-up
        :parameters (?paper - paper ?loc - loc)
        :precondition (and
            (at ?loc)
            (is_Home_Base ?loc)
            (unpacked ?paper)
        )
        :effect (and
            (not (unpacked ?paper))
            (carrying ?paper)
        )
    )

    (:action move
        :parameters (?from - loc ?to - loc)
        :precondition (and
            (at ?from)
        )
        :effect (and
            (not (at ?from))
            (at ?to)
        )
    )

    (:action deliver
        :parameters (?paper - paper ?loc - loc)
        :precondition (and
            (at ?loc)
            (wants_Paper ?loc)
            (carrying ?paper)
        )
        :effect (and
            (not (carrying ?paper))
            (not (wants_Paper ?loc))
            (satisfied ?loc)
        )
    )

)