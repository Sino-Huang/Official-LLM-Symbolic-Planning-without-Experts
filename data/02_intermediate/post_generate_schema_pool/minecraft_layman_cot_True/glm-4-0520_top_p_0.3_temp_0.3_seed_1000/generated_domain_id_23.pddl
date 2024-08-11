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
        :parameters (?arg0 - moveable ?arg1 - agent)
        :precondition (and
            (inventory ?arg0)
            (handsfree ?arg1)
        )
        :effect (and
            (not (inventory ?arg0))
            (equipped ?arg0 ?arg1)
        )
    )
    (:action recall
        :parameters (?item - moveable ?location - static)
        :precondition (and
            (at ?item ?location)
            (not (inventory ?item))
        )
        :effect (and
            (not (at ?item ?location))
            (inventory ?item)
            (not (equipped ?item ?agent))
            (handsfree ?agent)
        )
    )
    (:action pick
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and
            (at ?arg0 ?arg1)
            (agent_at ?arg1)
            (not (hypothetical ?arg0))
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
        )
    )
)