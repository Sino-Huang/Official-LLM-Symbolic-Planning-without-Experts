(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?agent - agent ?planks - moveable)
        :precondition (and (is_log ?log) (equipped ?log ?agent))
        :effect (and (not (equipped ?log ?agent)) (not (inventory ?log)) (inventory ?planks))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (equipped ?item ?agent) (not (handsfree ?agent)))
    )
     (:action move
        :parameters (?from_loc - static ?to_loc - static)
        :precondition (agent_at ?from_loc)
        :effect (and (not (agent_at ?from_loc)) (agent_at ?to_loc))
    )
     (:action pick
        :parameters (?item - moveable ?loc - static)
        :precondition (and (at ?item ?loc) (agent_at ?loc) (not (inventory ?item)))
        :effect (and (not (at ?item ?loc)) (inventory ?item))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (equipped ?item ?agent) (not (inventory ?item)))
        :effect (and (not (equipped ?item ?agent)) (inventory ?item) (handsfree ?agent))
    )
)