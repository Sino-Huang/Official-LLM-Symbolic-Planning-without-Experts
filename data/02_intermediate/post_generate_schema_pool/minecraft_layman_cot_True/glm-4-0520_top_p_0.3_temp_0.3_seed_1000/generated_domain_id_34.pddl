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
        )
    )
    (:action recall
        :parameters (?item - moveable ?loc - static ?agent - agent)
        :precondition (and
            (at ?item ?loc)
            (agent_at ?loc)
            (not (inventory ?item)) ; The item is not already in the inventory
        )
        :effect (and
            (inventory ?item)
            (not (at ?item ?loc))
            (handsfree ?agent) ; Assuming the agent is no longer holding the item
        )
    )
    (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and
            (at ?var0 ?var1)
            (agent_at ?var1)
            (not (hypothetical ?var0))
        )
        :effect (and
            (not (at ?var0 ?var1))
            (inventory ?var0)
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
            (is_log ?log)
            (inventory ?log)
            (handsfree ?agent)
        )
        :effect (and
            (not (is_log ?log))
            (is_planks ?plank)
            (inventory ?plank)
            (not (handsfree ?agent))
        )
    )
)