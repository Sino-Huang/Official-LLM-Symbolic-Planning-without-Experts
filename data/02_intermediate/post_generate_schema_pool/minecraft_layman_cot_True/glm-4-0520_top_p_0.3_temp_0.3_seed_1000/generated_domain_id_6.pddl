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
        :parameters (?o - moveable ?l - static)
        :precondition (and
            (at ?o ?l)
            (agent_at ?l)
            (not (hypothetical ?o))
        )
        :effect (and
            (not (at ?o ?l))
            (inventory ?o)
        )
    )
    (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and
            (at ?obj ?loc)
            (agent_at ?loc)
            (handsfree ?agent)
            (not (hypothetical ?obj))
        )
        :effect (and
            (not (at ?obj ?loc))
            (inventory ?obj)
            (not (handsfree ?agent))
        )
    )
    (:action move
        :parameters (?a - agent ?from - static ?to - static)
        :precondition (and
            (agent_at ?from)
        )
        :effect (and
            (not (agent_at ?from))
            (agent_at ?to)
        )
    )
    (:action craft_plank
        :parameters (?agent - agent ?log - moveable ?plank - moveable)
        :precondition (and
            (inventory ?log)
            (handsfree ?agent)
        )
        :effect (and
            (not (inventory ?log))
            (inventory ?plank)
            (not (handsfree ?agent))
            (equipped ?plank ?agent)
        )
    )
)