(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent)
        :precondition (and (is_log ?log) (inventory ?log) (handsfree ?agent))
        :effect (and (not (inventory ?log)) (inventory ?plank) (not (handsfree ?agent)) (equipped ?plank ?agent))
    )
     (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and (inventory ?var0) (handsfree ?var1))
        :effect (and (not (inventory ?var0)) (equipped ?var0 ?var1))
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
        :parameters (?item - moveable ?agent - agent)
        :precondition (equipped ?item ?agent)
        :effect (and (inventory ?item) (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)