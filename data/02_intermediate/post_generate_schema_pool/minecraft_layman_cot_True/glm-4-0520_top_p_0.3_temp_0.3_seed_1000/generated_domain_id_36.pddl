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
        :parameters (?obj - moveable ?loc - static ?agt - agent)
        :precondition (and
            (equipped ?obj ?agt)
            (handsfree ?agt)
        )
        :effect (and
            (not (at ?obj ?loc))
            (not (equipped ?obj ?agt))
            (inventory ?obj)
            (handsfree ?agt)
        )
    )
    (:action pick
        :parameters (?arg0 - moveable ?arg1 - static ?arg2 - agent)
        :precondition (and
            (at ?arg0 ?arg1)
            (agent_at ?arg1)
            (handsfree ?arg2)
        )
        :effect (and
            (not (at ?arg0 ?arg1))
            (inventory ?arg0)
            (equipped ?arg0 ?arg2)
        )
    )
    (:action move
        :parameters (?agent - agent ?var0 - static ?var1 - static)
        :precondition (and
            (agent_at ?var1)
        )
        :effect (and
            (not (agent_at ?var1))
            (agent_at ?var0)
        )
    )
    (:action craft_plank
        :parameters (?var0 - moveable ?var1 - moveable ?var2 - agent)
        :precondition (and
            (inventory ?var0)
            (handsfree ?var2)
        )
        :effect (and
            (inventory ?var1)
            (not (inventory ?var0))
        )
    )
)