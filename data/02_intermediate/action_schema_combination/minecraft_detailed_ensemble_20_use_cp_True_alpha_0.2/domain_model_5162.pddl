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
        :parameters (?agent - agent ?current_location - static ?destination - static)
        :precondition (agent_at ?current_location)
        :effect (and (not (agent_at ?current_location)) (agent_at ?destination))
    )
     (:action pick
        :parameters (?item - moveable ?loc - static)
        :precondition (and (agent_at ?loc) (at ?item ?loc) (not (hypothetical ?item)))
        :effect (and (not (at ?item ?loc)) (inventory ?item))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (equipped ?item ?agent) (inventory ?item))
        :effect (and (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)