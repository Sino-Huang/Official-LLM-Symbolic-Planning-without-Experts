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
        :parameters (?obj - moveable)
        :precondition (and
            (equipped ?obj ?agent) ;; The object is equipped by the agent
            (inventory ?obj) ;; The object can be placed in the inventory
        )
        :effect (and
            (not (at ?obj ?loc)) ;; The object is no longer at the location
            (not (equipped ?obj ?agent)) ;; The object is no longer equipped by the agent
            (inventory ?obj) ;; The object is now in the inventory
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
        :parameters (?agent - agent ?var0 - static ?var1 - static)
        :precondition (agent_at ?var1)
        :effect (and
            (not (agent_at ?var1))
            (agent_at ?var0)
        )
    )
    (:action craft_plank
        :parameters (?var0 - moveable ?var2 - moveable ?agent - agent)
        :precondition (and
            (inventory ?var2)
            (handsfree ?agent)
        )
        :effect (and
            (not (inventory ?var2))
            (inventory ?var0)
        )
    )
)