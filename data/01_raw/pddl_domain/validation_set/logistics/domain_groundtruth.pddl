(define (domain logistics)
    (:requirements :strips :typing)
    
    (:types 
        truck - object
        airplane - object
        location - object
        city - object
        airport - location
    )
    
    (:predicates
        (at ?obj - object ?loc - location)
        (in ?obj1 - object ?obj2 - object)
        (in-city ?loc - location ?city - city)
    )

    (:action load-truck
        :parameters (?obj - object ?truck - truck ?loc - location)
        :precondition (and (at ?truck ?loc) (at ?obj ?loc))
        :effect (and (not (at ?obj ?loc)) (in ?obj ?truck))
    )

    (:action load-airplane
        :parameters (?obj - object ?airplane - airplane ?loc - location)
        :precondition (and (at ?obj ?loc) (at ?airplane ?loc))
        :effect (and (not (at ?obj ?loc)) (in ?obj ?airplane))
    )

    (:action unload-truck
        :parameters (?obj - object ?truck - truck ?loc - location)
        :precondition (and (at ?truck ?loc) (in ?obj ?truck))
        :effect (and (not (in ?obj ?truck)) (at ?obj ?loc))
    )

    (:action unload-airplane
        :parameters (?obj - object ?airplane - airplane ?loc - location)
        :precondition (and (in ?obj ?airplane) (at ?airplane ?loc))
        :effect (and (not (in ?obj ?airplane)) (at ?obj ?loc))
    )

    (:action drive-truck
        :parameters (?truck - truck ?loc-from - location ?loc-to - location ?city - city)
        :precondition (and (at ?truck ?loc-from)
                           (in-city ?loc-from ?city)
                           (in-city ?loc-to ?city))
        :effect (and (not (at ?truck ?loc-from)) (at ?truck ?loc-to))
    )

    (:action fly-airplane
        :parameters (?airplane - airplane ?loc-from - airport ?loc-to - airport)
        :precondition (at ?airplane ?loc-from)
        :effect (and (not (at ?airplane ?loc-from)) (at ?airplane ?loc-to))
    )
)