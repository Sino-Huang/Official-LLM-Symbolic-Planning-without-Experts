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
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (not (handsfree ?agent)) (equipped ?item ?agent))
    )
     (:action move
        :parameters (?var0 - static ?var1 - static)
        :precondition (agent_at ?var1)
        :effect (and (not (agent_at ?var1)) (agent_at ?var0))
    )
     (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and (at ?var0 ?var1) (agent_at ?var1) (not (hypothetical ?var0)))
        :effect (and (not (at ?var0 ?var1)) (inventory ?var0))
    )
     (:action recall
        :parameters (?m - moveable ?a - agent ?l - static)
        :precondition (and (equipped ?m ?a) (not (inventory ?m)))
        :effect (and (inventory ?m) (not (equipped ?m ?a)) (handsfree ?a))
    )
)