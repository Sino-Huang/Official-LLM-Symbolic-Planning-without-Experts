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
        :parameters (?item - moveable ?agent - agent)
        :precondition (and
            (equipped ?item ?agent)
        )
        :effect (and
            (not (equipped ?item ?agent))
            (inventory ?item)
            (handsfree ?agent)
        )
    )
    (:action pick
        :parameters (?item - moveable ?loc - static)
        :precondition (and
            (agent_at ?loc)
            (at ?item ?loc)
            (not (hypothetical ?item))
        )
        :effect (and
            (not (at ?item ?loc))
            (inventory ?item)
            (equipped ?item ?agent) ; Assuming the agent equips the item upon picking it up
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
        :parameters (?log - moveable ?planks - moveable ?agent - agent)
        :precondition (and
            (is_log ?log)
            (equipped ?log ?agent)
        )
        :effect (and
            (not (equipped ?log ?agent))
            (inventory ?planks)
        )
    )
)