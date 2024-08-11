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
        :parameters (?item - moveable ?agent - agent)
        :precondition (and
            (inventory ?item)
            (handsfree ?agent)
        )
        :effect (and
            (not (inventory ?item))
            (equipped ?item ?agent)
            (not (handsfree ?agent))
        )
    )
    (:action recall
        :parameters (?item - moveable ?location - static)
        :precondition (and
            (equipped ?item ?agent)
            (agent_at ?location)
        )
        :effect (and
            (not (at ?item ?location))
            (not (equipped ?item ?agent))
            (inventory ?item)
            (handsfree ?agent)
        )
    )
    (:action pick
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and
            (agent_at ?arg1)
            (at ?arg0 ?arg1)
            (not (hypothetical ?arg0))
        )
        :effect (and
            (not (at ?arg0 ?arg1))
            (inventory ?arg0)
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
        :parameters (?log - moveable ?table - static ?plank - moveable)
        :precondition (and
            (is_log ?log)
            (at ?log ?table)
            (agent_at ?table)
        )
        :effect (and
            (inventory ?plank)
            (is_planks ?plank)
        )
    )
)