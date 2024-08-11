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
            (not (handsfree ?agent))
            (equipped ?item ?agent)
        )
    )
    (:action recall
        :parameters (?obj - moveable)
        :precondition (and
            (at ?obj ?loc)
            (agent_at ?loc)
        )
        :effect (and
            (not (at ?obj ?loc))
            (inventory ?obj)
        )
    )
    (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and
            (at ?obj ?loc)
            (agent_at ?loc)
            (not (hypothetical ?obj))
            (handsfree ?agent)
        )
        :effect (and
            (not (at ?obj ?loc))
            (inventory ?obj)
        )
    )
    (:action move
        :parameters (?from - static ?to - static)
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
            (is_log ?log)
        )
        :effect (and
            (not (inventory ?log))
            (inventory ?plank)
            (is_planks ?plank)
        )
    )
)