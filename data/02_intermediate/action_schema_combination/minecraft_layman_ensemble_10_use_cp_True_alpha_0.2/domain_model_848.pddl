(define (domain minecraft)
    (:requirements :negative-preconditions :strips :typing)
    (:types agent moveable static)
    (:predicates (agent_at ?arg0 - static)  (at ?arg0 - moveable ?arg1 - static)  (equipped ?arg0 - moveable ?arg1 - agent)  (handsfree ?arg0 - agent)  (hypothetical ?arg0 - moveable)  (inventory ?arg0 - moveable)  (is_grass ?arg0 - moveable)  (is_log ?arg0 - moveable)  (is_planks ?arg0 - moveable))
    (:action craft_plank
        :parameters (?log - moveable ?table - static ?plank - moveable)
        :precondition (and (is_log ?log) (at ?log ?table) (agent_at ?table))
        :effect (and (inventory ?plank) (is_planks ?plank))
    )
     (:action equip
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (inventory ?item) (handsfree ?agent))
        :effect (and (not (inventory ?item)) (equipped ?item ?agent) (not (handsfree ?agent)))
    )
     (:action move
        :parameters (?agent - agent ?var0 - static ?var1 - static)
        :precondition (agent_at ?var1)
        :effect (and (not (agent_at ?var1)) (agent_at ?var0))
    )
     (:action pick
        :parameters (?obj - moveable ?loc - static)
        :precondition (and (at ?obj ?loc) (agent_at ?loc))
        :effect (and (not (at ?obj ?loc)) (inventory ?obj))
    )
     (:action recall
        :parameters (?item - moveable ?agent - agent)
        :precondition (and (equipped ?item ?agent) (inventory ?item))
        :effect (and (not (equipped ?item ?agent)) (inventory ?item))
    )
)