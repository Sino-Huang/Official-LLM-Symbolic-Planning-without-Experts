(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?agent - agent ?log - moveable ?plank - moveable)
        :precondition (and (inventory ?log) (handsfree ?agent))
        :effect (and (not (inventory ?log)) (inventory ?plank) (not (handsfree ?agent)) (equipped ?plank ?agent))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (not (handsfree ?agent)) (equipped ?item ?agent))
    )
     (:action move
        :parameters (?from - static ?to - static)
        :precondition (agent_at ?from)
        :effect (and (not (agent_at ?from)) (agent_at ?to))
    )
     (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and (at ?var0 ?var1) (agent_at ?var1))
        :effect (inventory ?var0)
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent ?location - static)
        :precondition (and (at ?item ?location) (equipped ?item ?agent))
        :effect (and (inventory ?item) (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)