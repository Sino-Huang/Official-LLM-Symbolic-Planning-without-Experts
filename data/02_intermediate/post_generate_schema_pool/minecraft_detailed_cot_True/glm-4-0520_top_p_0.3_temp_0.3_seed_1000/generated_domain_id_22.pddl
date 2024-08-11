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
        :parameters (?item - moveable ?agent - agent)
        :precondition (and
            (equipped ?item ?agent) ;; The agent must be holding the item to recall it.
        )
        :effect (and
            (not (equipped ?item ?agent)) ;; The item is no longer equipped after the recall action.
            (inventory ?item) ;; The item is now in the agent's inventory.
            (handsfree ?agent) ;; The agent's hands are free after recalling the item.
        )
    )
    (:action pick
        :parameters (?item - moveable ?location - static ?agent - agent)
        :precondition (and
            (at ?item ?location)
            (agent_at ?location)
            (handsfree ?agent)
        )
        :effect (and
            (inventory ?item)
            (not (at ?item ?location))
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
        :parameters (?agent - agent ?log - moveable ?agent - agent ?log - moveable ?planks - moveable)
        :precondition (and
            (equipped ?log ?agent)
        )
        :effect (and
            (not (equipped ?log ?agent))
            (inventory ?planks)
            (not (inventory ?log))
            (is_planks ?planks)
            (not (is_log ?log))
        )
    )
)