(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?planks - moveable ?agent - agent)
        :precondition (and (is_log ?log) (equipped ?log ?agent))
        :effect (and (not (equipped ?log ?agent)) (inventory ?planks) (handsfree ?agent))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (equipped ?item ?agent) (not (handsfree ?agent)))
    )
     (:action move
        :parameters (?agent - agent ?from - static ?to - static)
        :precondition (agent_at ?from)
        :effect (and (not (agent_at ?from)) (agent_at ?to))
    )
     (:action pick
        :parameters (?item - moveable ?loc - static)
        :precondition (and (at ?item ?loc) (agent_at ?loc) (not (hypothetical ?item)))
        :effect (and (not (at ?item ?loc)) (inventory ?item))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (equipped ?item ?agent)
        :effect (and (inventory ?item) (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)