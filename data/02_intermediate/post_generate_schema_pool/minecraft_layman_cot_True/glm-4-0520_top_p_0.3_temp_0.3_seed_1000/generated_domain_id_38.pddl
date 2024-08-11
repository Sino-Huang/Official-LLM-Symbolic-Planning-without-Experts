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
            (at ?item ?location)
            (agent_at ?location)
            (not (hypothetical ?item))
        )
        :effect (and
            (not (at ?item ?location))
            (inventory ?item)
        )
    )
    (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and
            (at ?obj ?loc)
            (agent_at ?loc)
            (handsfree ?agent)
        )
        :effect (and
            (not (at ?obj ?loc))
            (inventory ?obj)
            (not (handsfree ?agent))
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
        :parameters (?var0 - moveable ?var1 - moveable ?var2 - agent)
        :precondition (and
            (equipped ?var0 ?var2)
            (handsfree ?var2)
        )
        :effect (and
            (not (inventory ?var0))
            (not (equipped ?var0 ?var2))
            (inventory ?var1)
        )
    )
)