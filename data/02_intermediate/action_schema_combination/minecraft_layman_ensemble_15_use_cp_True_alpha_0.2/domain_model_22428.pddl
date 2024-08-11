(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?table - static ?plank - moveable)
        :precondition (and (is_log ?log) (at ?log ?table) (agent_at ?table))
        :effect (and (inventory ?plank) (is_planks ?plank))
    )
     (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and (inventory ?var0) (handsfree ?var1))
        :effect (and (not (inventory ?var0)) (equipped ?var0 ?var1) (not (handsfree ?var1)))
    )
     (:action move
        :parameters (?arg0 - static ?arg1 - static)
        :precondition (agent_at ?arg1)
        :effect (and (not (agent_at ?arg1)) (agent_at ?arg0))
    )
     (:action pick
        :parameters (?arg0 - moveable ?arg1 - static ?arg2 - agent)
        :precondition (and (agent_at ?arg1) (at ?arg0 ?arg1) (handsfree ?arg2))
        :effect (and (not (at ?arg0 ?arg1)) (inventory ?arg0) (not (handsfree ?arg2)) (equipped ?arg0 ?arg2))
    )
     (:action recall
        :parameters (?item - moveable ?location - static)
        :precondition (and (at ?item ?location) (agent_at ?location) (not (inventory ?item)))
        :effect (and (not (at ?item ?location)) (inventory ?item))
    )
)