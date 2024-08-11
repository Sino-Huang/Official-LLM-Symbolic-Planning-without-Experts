(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?planks - moveable ?agent - agent)
        :precondition (equipped ?log ?agent)
        :effect (and (not (equipped ?log ?agent)) (inventory ?planks))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (not (handsfree ?agent)) (equipped ?item ?agent))
    )
     (:action move
        :parameters (?agent - agent ?current_location - static ?destination - static)
        :precondition (agent_at ?current_location)
        :effect (and (not (agent_at ?current_location)) (agent_at ?destination))
    )
     (:action pick
        :parameters (?item - moveable ?location - static ?agent - agent)
        :precondition (and (at ?item ?location) (agent_at ?location) (handsfree ?agent))
        :effect (and (not (at ?item ?location)) (inventory ?item))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (equipped ?item ?agent) (inventory ?item))
        :effect (and (not (equipped ?item ?agent)) (handsfree ?agent))
    )
)