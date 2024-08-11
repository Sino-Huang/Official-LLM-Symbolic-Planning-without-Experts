(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?agent - agent)
        :precondition (and (equipped ?log ?agent) (handsfree ?agent))
        :effect (and (not (is_log ?log)) (is_planks ?log) (inventory ?log))
    )
     (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and (inventory ?var0) (handsfree ?var1))
        :effect (and (equipped ?var0 ?var1) (not (handsfree ?var1)))
    )
     (:action move
        :parameters (?arg0 - static ?arg1 - static)
        :precondition (agent_at ?arg1)
        :effect (and (not (agent_at ?arg1)) (agent_at ?arg0))
    )
     (:action pick
        :parameters (?obj - moveable ?loc - static ?agent - agent)
        :precondition (and (at ?obj ?loc) (handsfree ?agent))
        :effect (and (not (at ?obj ?loc)) (inventory ?obj))
    )
     (:action recall
        :parameters (?item - moveable ?location - static)
        :precondition (and (at ?item ?location) (agent_at ?location) (not (inventory ?item)))
        :effect (and (not (at ?item ?location)) (inventory ?item))
    )
)