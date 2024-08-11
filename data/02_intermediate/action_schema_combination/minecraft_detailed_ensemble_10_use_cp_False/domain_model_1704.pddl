(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?planks - moveable ?agent - agent)
        :precondition (and (equipped ?log ?agent) (not (hypothetical ?log)))
        :effect (and (not (equipped ?log ?agent)) (inventory ?planks))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (not (handsfree ?agent)) (equipped ?item ?agent) (not (hypothetical ?item)))
    )
     (:action move
        :parameters (?start_loc - static ?end_loc - static)
        :precondition (agent_at ?start_loc)
        :effect (and (not (agent_at ?start_loc)) (agent_at ?end_loc))
    )
     (:action pick
        :parameters (?item - moveable ?loc - static)
        :precondition (and (agent_at ?loc) (at ?item ?loc) (not (hypothetical ?item)))
        :effect (and (not (at ?item ?loc)) (inventory ?item))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (equipped ?item ?agent) (not (inventory ?item)))
        :effect (and (not (equipped ?item ?agent)) (inventory ?item) (handsfree ?agent))
    )
)