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
        :parameters (?arg0 - moveable ?arg1 - agent)
        :precondition (and (inventory ?arg0) (handsfree ?arg1))
        :effect (and (not (inventory ?arg0)) (equipped ?arg0 ?arg1))
    )
     (:action move
        :parameters (?agent - agent ?from - static ?to - static)
        :precondition (agent_at ?from)
        :effect (and (not (agent_at ?from)) (agent_at ?to))
    )
     (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and (at ?var0 ?var1) (agent_at ?var1))
        :effect (and (not (at ?var0 ?var1)) (inventory ?var0))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (equipped ?item ?agent)
        :effect (and (inventory ?item) (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)