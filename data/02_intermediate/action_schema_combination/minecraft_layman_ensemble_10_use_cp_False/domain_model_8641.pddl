(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent)
        :precondition (and (inventory ?log) (is_log ?log))
        :effect (and (not (inventory ?log)) (inventory ?plank) (is_planks ?plank))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (equipped ?item ?agent) (not (handsfree ?agent)))
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
        :parameters (?item - moveable ?loc - static ?agent - agent)
        :precondition (and (at ?item ?loc) (agent_at ?loc) (not (inventory ?item)))
        :effect (and (inventory ?item) (not (at ?item ?loc)) (handsfree ?agent))
    )
)