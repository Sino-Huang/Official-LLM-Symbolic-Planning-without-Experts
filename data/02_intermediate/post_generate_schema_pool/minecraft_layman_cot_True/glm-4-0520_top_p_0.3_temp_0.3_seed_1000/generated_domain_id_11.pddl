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
            (not (handsfree ?arg1))
        )
    )
    (:action recall
        :parameters (?item - moveable ?location - static ?agent - agent)
        :precondition (and
            (equipped ?item ?agent)
        )
        :effect (and
            (not (at ?item ?location))
            (not (equipped ?item ?agent))
            (inventory ?item)
            (handsfree ?agent)
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
            (equipped ?obj ?agent)
            (not (handsfree ?agent))
        )
    )
    (:action move
        :parameters (?var0 - static ?var1 - static)
        :precondition (and
            (agent_at ?var1)
        )
        :effect (and
            (agent_at ?var0)
            (not (agent_at ?var1))
        )
    )
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent)
        :precondition (and
            (inventory ?log)
            (handsfree ?agent)
        )
        :effect (and
            (not (inventory ?log))
            (inventory ?plank)
        )
    )
)