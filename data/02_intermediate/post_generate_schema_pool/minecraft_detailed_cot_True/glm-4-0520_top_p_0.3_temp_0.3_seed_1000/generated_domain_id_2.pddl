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
        :precondition (equipped ?item ?agent)
        :effect (and
            (not (equipped ?item ?agent))
            (inventory ?item)
            (handsfree ?agent)
        )
    )
    (:action pick
        :parameters (?item - moveable)
        :precondition (and
            (at ?item ?loc)        ;; The item is at a location
            (agent_at ?loc)        ;; The agent is at the same location as the item
            (not (inventory ?item)) ;; The item is not already in the agent's inventory
        )
        :effect (and
            (not (at ?item ?loc))   ;; The item is no longer at its previous location
            (inventory ?item)       ;; The item is now in the agent's inventory
        )
    )
    (:action move
        :parameters (?start - static ?end - static)
        :precondition (and
            (agent_at ?start)
        )
        :effect (and
            (not (agent_at ?start))
            (agent_at ?end)
        )
    )
    (:action craft_plank
        :parameters (?log - moveable ?agent - agent)
        :precondition (and
            (is_log ?log)
            (equipped ?log ?agent)
        )
        :effect (and
            (not (equipped ?log ?agent))
            (inventory ?planks) ;; Here, ?planks is a new variable representing the planks created from the log
            (not (is_log ?log)) ;; This indicates that the log has been used up in the crafting process
        )
    )
)