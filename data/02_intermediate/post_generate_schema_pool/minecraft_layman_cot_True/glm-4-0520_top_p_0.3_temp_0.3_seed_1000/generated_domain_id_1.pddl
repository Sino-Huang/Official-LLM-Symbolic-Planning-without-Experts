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
        :parameters (?obj - moveable ?agent - agent ?loc - static)
        :precondition (and 
            (equipped ?obj ?agent)
        )
        :effect (and
            (not (at ?obj ?loc))
            (not (equipped ?obj ?agent))
            (inventory ?obj)
        )
    )
    (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and
            (at ?var0 ?var1)
            (agent_at ?var1)
        )
        :effect (and
            (not (at ?var0 ?var1))
            (inventory ?var0)
        )
    )
    (:action move
        :parameters (?var0 - static ?var1 - static)
        :precondition (and
            (agent_at ?var1) ;; The agent must be at the starting location
        )
        :effect (and
            (not (agent_at ?var1)) ;; The agent is no longer at the starting location
            (agent_at ?var0) ;; The agent is now at the destination location
        )
    )
    (:action craft_plank
        :parameters (?var0 - moveable ?var2 - moveable)
        :precondition (and
            (is_log ?var0)
            (is_log ?var2)
            (inventory ?var2)
        )
        :effect (and
            (not (inventory ?var2))
            (hypothetical ?var0)
            (is_planks ?var0)
        )
    )
)