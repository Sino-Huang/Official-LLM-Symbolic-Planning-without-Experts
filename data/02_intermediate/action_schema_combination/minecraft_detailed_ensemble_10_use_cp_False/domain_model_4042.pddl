(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?agent - agent)
        :precondition (and (is_log ?log) (equipped ?log ?agent) (handsfree ?agent))
        :effect (and (not (is_log ?log)) (not (equipped ?log ?agent)) (is_planks ?log))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (equipped ?item ?agent) (not (handsfree ?agent)))
    )
     (:action move
        :parameters (?start - static ?end - static)
        :precondition (agent_at ?start)
        :effect (and (not (agent_at ?start)) (agent_at ?end))
    )
     (:action pick
        :parameters (?item - moveable ?location - static)
        :precondition (and (at ?item ?location) (agent_at ?location))
        :effect (and (not (at ?item ?location)) (inventory ?item))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (equipped ?item ?agent) (inventory ?item))
        :effect (and (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)