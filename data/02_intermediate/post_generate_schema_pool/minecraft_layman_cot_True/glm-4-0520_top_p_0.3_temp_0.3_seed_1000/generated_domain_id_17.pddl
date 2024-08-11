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
        :parameters (?obj - moveable ?agent - agent)
        :precondition (and
            (equipped ?obj ?agent)
            (not (hypothetical ?obj))
        )
        :effect (and
            (not (equipped ?obj ?agent))
            (inventory ?obj)
            (handsfree ?agent)
        )
    )
    (:action pick
        :parameters (?arg0 - moveable ?arg1 - static ?arg2 - agent)
        :precondition (and
            (agent_at ?arg1)
            (at ?arg0 ?arg1)
            (handsfree ?arg2)
        )
        :effect (and
            (not (at ?arg0 ?arg1))
            (inventory ?arg0)
            (not (handsfree ?arg2))
            (equipped ?arg0 ?arg2)
        )
    )
    (:action move
        :parameters (?agent - agent ?from - static ?to - static)
        :precondition (agent_at ?from)
        :effect (and
            (not (agent_at ?from))
            (agent_at ?to)
        )
    )
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent)
        :precondition (and
            (inventory ?log)
            (handsfree ?agent)
        )
        :effect (and
            (not (inventory ?log))
            (inventory ?plank)
        )
    )
)