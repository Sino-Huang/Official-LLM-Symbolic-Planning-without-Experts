(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent)
        :precondition (and (inventory ?log) (handsfree ?agent))
        :effect (and (not (inventory ?log)) (inventory ?plank))
    )
     (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and (inventory ?var0) (handsfree ?var1))
        :effect (and (not (inventory ?var0)) (not (handsfree ?var1)) (equipped ?var0 ?var1))
    )
     (:action move
        :parameters (?from - static ?to - static)
        :precondition (agent_at ?from)
        :effect (and (not (agent_at ?from)) (agent_at ?to))
    )
     (:action pick
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and (agent_at ?arg1) (at ?arg0 ?arg1) (not (hypothetical ?arg0)))
        :effect (and (not (at ?arg0 ?arg1)) (inventory ?arg0))
    )
     (:action recall
        :parameters (?item - moveable ?loc - static ?agent - agent)
        :precondition (and (at ?item ?loc) (agent_at ?loc) (not (inventory ?item)))
        :effect (and (inventory ?item) (not (at ?item ?loc)) (handsfree ?agent))
    )
)