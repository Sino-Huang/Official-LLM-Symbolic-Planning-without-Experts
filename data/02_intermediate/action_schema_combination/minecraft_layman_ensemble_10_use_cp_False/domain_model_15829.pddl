(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?plank - moveable ?agent - agent)
        :precondition (and (is_log ?log) (inventory ?log) (handsfree ?agent))
        :effect (and (not (is_log ?log)) (is_planks ?plank) (inventory ?plank))
    )
     (:action equip
        :parameters (?arg0 - moveable ?arg1 - agent)
        :precondition (and (inventory ?arg0) (handsfree ?arg1))
        :effect (and (not (inventory ?arg0)) (equipped ?arg0 ?arg1))
    )
     (:action move
        :parameters (?from - static ?to - static)
        :precondition (agent_at ?from)
        :effect (and (not (agent_at ?from)) (agent_at ?to))
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