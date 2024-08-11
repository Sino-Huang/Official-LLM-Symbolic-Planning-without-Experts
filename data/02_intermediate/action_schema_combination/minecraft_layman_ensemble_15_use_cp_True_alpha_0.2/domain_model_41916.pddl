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
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and (agent_at ?arg1) (at ?arg0 ?arg1) (not (hypothetical ?arg0)))
        :effect (and (not (at ?arg0 ?arg1)) (inventory ?arg0))
    )
     (:action recall
        :parameters (?obj - moveable ?agent - agent)
        :precondition (and (equipped ?obj ?agent) (not (hypothetical ?obj)))
        :effect (and (not (equipped ?obj ?agent)) (inventory ?obj) (handsfree ?agent))
    )
)