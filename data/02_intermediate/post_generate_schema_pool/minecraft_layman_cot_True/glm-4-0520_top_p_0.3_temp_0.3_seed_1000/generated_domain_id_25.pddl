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
        :parameters (?item - moveable ?location - static ?agent - agent)
        :precondition (and
            (at ?item ?location) ;; The item is at a location in the world
            (agent_at ?location) ;; The agent is at the same location as the item
        )
        :effect (and
            (not (at ?item ?location)) ;; The item is no longer at the location
            (inventory ?item) ;; The item is now in the agent's inventory
        )
    )
    (:action pick
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and
            (at ?arg0 ?arg1)
            (agent_at ?arg1)
        )
        :effect (and
            (not (at ?arg0 ?arg1))
            (inventory ?arg0)
        )
    )
    (:action move
        :parameters (?var0 - static ?var1 - static)
        :precondition (agent_at ?var1)
        :effect (and
            (not (agent_at ?var1))
            (agent_at ?var0)
        )
    )
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent ?location - static)
        :precondition (and
            (is_log ?log)
            (inventory ?log ?agent)
            (agent_at ?location)
        )
        :effect (and
            (not (inventory ?log ?agent))
            (is_planks ?plank)
            (inventory ?plank ?agent)
        )
    )
)