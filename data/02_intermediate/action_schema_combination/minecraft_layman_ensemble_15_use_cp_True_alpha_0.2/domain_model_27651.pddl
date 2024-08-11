(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent ?location - static)
        :precondition (and (is_log ?log) (inventory ?log) (handsfree ?agent))
        :effect (and (not (inventory ?log)) (not (at ?log ?location)) (inventory ?plank))
    )
     (:action equip
        :parameters (?arg0 - moveable ?arg1 - agent)
        :precondition (and (inventory ?arg0) (handsfree ?arg1))
        :effect (and (not (inventory ?arg0)) (equipped ?arg0 ?arg1) (not (handsfree ?arg1)))
    )
     (:action move
        :parameters (?var0 - static ?var1 - static)
        :precondition (agent_at ?var1)
        :effect (and (agent_at ?var0) (not (agent_at ?var1)))
    )
     (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and (at ?obj ?loc) (agent_at ?loc) (not (hypothetical ?obj)))
        :effect (and (not (at ?obj ?loc)) (inventory ?obj))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (equipped ?item ?agent)
        :effect (and (inventory ?item) (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)