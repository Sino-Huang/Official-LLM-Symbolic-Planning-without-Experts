(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent)
        :precondition (and (is_log ?log) (inventory ?log) (handsfree ?agent))
        :effect (and (not (inventory ?log)) (inventory ?plank))
    )
     (:action equip
        :parameters (?var0 - moveable ?var1 - agent)
        :precondition (and (inventory ?var0) (handsfree ?var1))
        :effect (and (not (inventory ?var0)) (equipped ?var0 ?var1) (not (handsfree ?var1)))
    )
     (:action move
        :parameters (?a - agent ?from - static ?to - static)
        :precondition (agent_at ?from)
        :effect (and (not (agent_at ?from)) (agent_at ?to))
    )
     (:action pick
        :parameters (?var0 - moveable ?var1 - static)
        :precondition (and (at ?var0 ?var1) (agent_at ?var1))
        :effect (and (not (at ?var0 ?var1)) (inventory ?var0) (not (hypothetical ?var0)))
    )
     (:action recall
        :parameters (?item - moveable ?location - static)
        :precondition (and (at ?item ?location) (agent_at ?location))
        :effect (and (not (at ?item ?location)) (inventory ?item))
    )
)