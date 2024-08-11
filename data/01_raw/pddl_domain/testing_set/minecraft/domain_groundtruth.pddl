
(define (domain minecraft)
    (:requirements :strips :typing)
    (:types
        moveable static agent
    )
    (:predicates ; predicates refer to the preperties of the objects
        (is_grass ?arg0 - moveable)
        (is_log ?arg0 - moveable)
        (is_planks ?arg0 - moveable)
        (at ?arg0 - moveable ?arg1 - static)
        (agent_at ?arg0 - static)
        (inventory ?arg0 - moveable)
        (hypothetical ?arg0 - moveable)
        (equipped ?arg0 - moveable ?arg1 - agent)
        (handsfree ?arg0 - agent)
    )

    ; (:actions recall move craft_plank equip pick)

    (:action recall
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and
            (equipped ?var0 ?var1)
        )
        :effect (and
            (inventory ?var0)
            (not (equipped ?var0 ?var1))
            (handsfree ?var1)
        )
    )

    (:action move
        :parameters (?var0 - static ?var1 - static)
        :precondition (and
            (agent_at ?var1)
        )
        :effect (and
            (agent_at ?var0)
            (not (agent_at ?var1))
        )
    )

    (:action craft_plank
        :parameters (?var0 - moveable ?var1 - agent ?var2 - moveable)
        :precondition (and
            (hypothetical ?var0)
            (is_log ?var2)
            (equipped ?var2 ?var1)
        )
        :effect (and
            (inventory ?var0)
            (is_planks ?var0)
            (handsfree ?var1)
            (not (equipped ?var2 ?var1))
            (not (hypothetical ?var0))
            (not (is_log ?var2))
        )
    )

    (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and
            (inventory ?var0)
            (handsfree ?var1)
        )
        :effect (and
            (equipped ?var0 ?var1)
            (not (handsfree ?var1))
            (not (inventory ?var0))
        )
    )

    (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and
            (at ?var0 ?var1)
            (agent_at ?var1)
        )
        :effect (and
            (inventory ?var0)
            (not (at ?var0 ?var1))
        )
    )
)