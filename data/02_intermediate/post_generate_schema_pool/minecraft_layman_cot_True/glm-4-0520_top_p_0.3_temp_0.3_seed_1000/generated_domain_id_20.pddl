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
        :parameters (?item - moveable ?agent - agent ?location - static)
        :precondition (and
            (handsfree ?agent)
            (equipped ?item ?agent)
        )
        :effect (and
            (not (at ?item ?location))
            (inventory ?item)
            (not (handsfree ?agent))
        )
    )
    (:action pick
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and
            (at ?arg0 ?arg1)
            (agent_at ?arg1)
            (handsfree ?arg0)
        )
        :effect (and
            (not (at ?arg0 ?arg1))
            (inventory ?arg0)
            (not (hypothetical ?arg0))
            (not (handsfree ?arg0))
            (equipped ?arg0 ?arg0)
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
            (inventory ?log)
            (handsfree ?agent)
        )
        :effect (and
            (inventory ?plank)
            (not (inventory ?log))
            (equipped ?plank ?agent)
        )
    )
)