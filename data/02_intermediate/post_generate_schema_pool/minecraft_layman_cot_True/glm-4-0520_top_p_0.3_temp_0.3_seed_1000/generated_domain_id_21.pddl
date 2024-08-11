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
            (not (handsfree ?var1))
            (equipped ?var0 ?var1)
        )
    )
    (:action recall
        :parameters (?obj - moveable ?loc - static ?agent - agent)
        :precondition (and
            (at ?obj ?loc)
            (agent_at ?loc)
            (handsfree ?agent)
        )
        :effect (and
            (not (at ?obj ?loc))
            (inventory ?obj)
        )
    )
    (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and
            (at ?obj ?loc)
            (agent_at ?loc)
        )
        :effect (and
            (not (at ?obj ?loc))
            (inventory ?obj)
        )
    )
    (:action move
        :parameters (?arg0 - static ?arg1 - static)
        :precondition (and
            (agent_at ?arg0)
        )
        :effect (and
            (not (agent_at ?arg0))
            (agent_at ?arg1)
        )
    )
    (:action craft_plank
        :parameters (?var0 - moveable ?var1 - moveable ?var2 - agent)
        :precondition (and
            (is_log ?var1)
            (inventory ?var1)
            (handsfree ?var2)
        )
        :effect (and
            (not (inventory ?var1))
            (inventory ?var0)
        )
    )
)