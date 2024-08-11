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
    (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and
            (at ?var0 ?var1)  ;; The object must be at the location
            (agent_at ?var1)  ;; The agent must be at the location
        )
        :effect (and
            (not (at ?var0 ?var1))  ;; The object is no longer at the location
            (inventory ?var0)       ;; The object is now in the agent's inventory
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
            (hypothetical ?plank)
        )
        :effect (and
            (not (inventory ?log))
            (inventory ?plank)
            (not (hypothetical ?plank))
        )
    )
)