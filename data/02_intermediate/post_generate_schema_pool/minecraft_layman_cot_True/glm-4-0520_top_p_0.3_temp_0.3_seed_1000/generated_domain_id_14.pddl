(define (domain minecraft)

    (:requirements :strips :typing :negative-preconditions)

    (:types
    moveable static agent
)

    (:predicates
        (is_grass ?arg0 - moveable) ;; the object is grass
        (is_log ?arg0 - moveable) ;; the object is a log
        (is_planks ?arg0 - moveable) ;; the object is a plank
        (at ?arg0 - moveable ?arg1 - static) ;; the object is at a location
        (agent_at ?arg0 - static) ;; the agent is at a location
        (inventory ?arg0 - moveable) ;; the object is in the agent's inventory
        (hypothetical ?arg0 - moveable) ;; the object is hypothetical
        (equipped ?arg0 - moveable ?arg1 - agent) ;; the agent is holding the object
        (handsfree ?arg0 - agent) ;; the agent has empty hands
    )

    (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and
            (inventory ?var0)
            (handsfree ?var1)
        )
        :effect (and
            (not (inventory ?var0))
            (equipped ?var0 ?var1)
            (not (handsfree ?var1))
        )
    )
    (:action recall
        :parameters (?m - moveable ?a - agent ?l - static)
        :precondition (and
            (equipped ?m ?a)
            (not (inventory ?m))
        )
        :effect (and
            (inventory ?m)
            (not (equipped ?m ?a))
            (handsfree ?a)
        )
    )
    (:action pick
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and
            (at ?arg0 ?arg1)
            (agent_at ?arg1)
            (handsfree ?arg0)
        )
        :effect (and
            (not (at ?arg0 ?arg1))
            (inventory ?arg0)
            (not (handsfree ?arg0))
        )
    )
    (:action move
        :parameters (?agent - agent ?from - static ?to - static)
        :precondition (and
            (agent_at ?from)
        )
        :effect (and
            (not (agent_at ?from))
            (agent_at ?to)
        )
    )
    (:action craft_plank
        :parameters (?arg1 - agent ?var0 - moveable ?var2 - moveable)
        :precondition (and
            (inventory ?var0)
            (handsfree ?arg1)
            (agent_at ?arg1)
            (is_log ?var0)
            (at ?var2 ?arg1)
        )
        :effect (and
            (not (inventory ?var0))
            (inventory ?var0) ;; Assuming var0 now represents the plank
            (not (is_log ?var0))
            (is_planks ?var0)
        )
    )
)