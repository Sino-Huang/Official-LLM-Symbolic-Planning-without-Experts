(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?var0 - moveable ?var2 - moveable ?agent - agent)
        :precondition (and (inventory ?var2) (handsfree ?agent))
        :effect (and (not (inventory ?var2)) (inventory ?var0))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (not (handsfree ?agent)) (equipped ?item ?agent))
    )
     (:action move
        :parameters (?start - static ?destination - static)
        :precondition (agent_at ?start)
        :effect (and (not (agent_at ?start)) (agent_at ?destination))
    )
     (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and (at ?obj ?loc) (agent_at ?loc))
        :effect (and (not (at ?obj ?loc)) (inventory ?obj))
    )
     (:action recall
        :parameters (?arg0 - moveable ?arg1 - static)
        :precondition (and (at ?arg0 ?arg1) (agent_at ?arg1))
        :effect (and (not (at ?arg0 ?arg1)) (inventory ?arg0))
    )
)