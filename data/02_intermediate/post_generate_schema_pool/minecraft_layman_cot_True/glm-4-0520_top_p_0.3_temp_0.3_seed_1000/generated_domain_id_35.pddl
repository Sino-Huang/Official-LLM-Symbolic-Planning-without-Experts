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
        :parameters (?obj - moveable ?agent - agent)
        :precondition (and
            (inventory ?obj)
            (handsfree ?agent)
        )
        :effect (and
            (not (inventory ?obj))
            (not (handsfree ?agent))
            (equipped ?obj ?agent)
        )
    )
    (:action recall
        :parameters (?obj - moveable ?agent - agent ?loc - static)
        :precondition (and
            (equipped ?obj ?agent)
            (handsfree ?agent)
        )
        :effect (and
            (not (at ?obj ?loc))
            (not (equipped ?obj ?agent))
            (inventory ?obj)
        )
    )
    (:action pick
        :parameters (?var0 - moveable ?var1 - static ?var2 - agent)
        :precondition (and
            (at ?var0 ?var1)
            (agent_at ?var1)
            (handsfree ?var2)
        )
        :effect (and
            (not (at ?var0 ?var1))
            (inventory ?var0)
            (not (handsfree ?var2))
            (equipped ?var0 ?var2)
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
        :parameters (?agent - agent ?log - moveable ?plank - moveable)
        :precondition (and
            (is_log ?log)
            (equipped ?agent ?log)
        )
        :effect (and
            (is_planks ?plank)
            (inventory ?plank)
            (not (inventory ?log))
            (not (equipped ?agent ?log))
        )
    )
)