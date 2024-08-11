(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?var0 - moveable ?var2 - moveable)
        :precondition (and (is_log ?var0) (is_log ?var2) (inventory ?var2))
        :effect (and (not (inventory ?var2)) (hypothetical ?var0) (is_planks ?var0))
    )
     (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and (inventory ?var0) (handsfree ?var1))
        :effect (and (equipped ?var0 ?var1) (not (handsfree ?var1)))
    )
     (:action move
        :parameters (?var0 - static ?var1 - static)
        :precondition (agent_at ?var1)
        :effect (and (agent_at ?var0) (not (agent_at ?var1)))
    )
     (:action pick
        :parameters (?arg0 - moveable ?arg1 - static ?arg2 - agent)
        :precondition (and (agent_at ?arg1) (at ?arg0 ?arg1) (handsfree ?arg2))
        :effect (and (not (at ?arg0 ?arg1)) (inventory ?arg0) (not (handsfree ?arg2)) (equipped ?arg0 ?arg2))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (equipped ?item ?agent) (not (handsfree ?agent)))
        :effect (and (not (equipped ?item ?agent)) (inventory ?item) (handsfree ?agent))
    )
)