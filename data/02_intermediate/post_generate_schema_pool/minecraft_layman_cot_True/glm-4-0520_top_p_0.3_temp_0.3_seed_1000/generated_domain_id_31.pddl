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
        :parameters (?item - moveable ?agent - agent)
        :precondition (and
            (equipped ?item ?agent)
        )
        :effect (and
            (inventory ?item)
            (not (equipped ?item ?agent))
            (handsfree ?agent)
        )
    )
    (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and
            (at ?obj ?loc)
            (agent_at ?loc)
            (handsfree ?agent) ;; Assuming ?agent is a parameter representing the agent performing the action
        )
        :effect (and
            (not (at ?obj ?loc))
            (inventory ?obj)
        )
    )
    (:action move
        :parameters (?start - static ?destination - static)
        :precondition (and
            (agent_at ?start)
        )
        :effect (and
            (not (agent_at ?start))
            (agent_at ?destination)
        )
    )
    (:action craft_plank
        :parameters (?log - moveable ?agent - agent)
        :precondition (and
            (equipped ?log ?agent)  ;; The log must be in the agent's inventory or equipped by the agent
            (handsfree ?agent)  ;; The agent must have free hands to perform the crafting
        )
        :effect (and
            (not (is_log ?log))  ;; The log is no longer a log after crafting
            (is_planks ?log)  ;; The log is now a plank
            (inventory ?log)  ;; The plank is now in the agent's inventory
        )
    )
)