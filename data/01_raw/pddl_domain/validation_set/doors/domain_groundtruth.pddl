(define (domain doors)
  (:requirements :strips :typing)
  (:types
    location room key
  )
  (:predicates
    (at ?loc - location)
    (unlocked ?room - room)

    (loc_in_room ?loc - location ?room - room)

    (key_at ?key - key ?loc - location)

    (key_for_room ?key - key ?room - room)
  )

  ; (:actions move_to pick)

  (:action move_to
    :parameters (?sloc - location ?eloc - location ?eroom - room)
    :precondition (and
      (at ?sloc)
      (unlocked ?eroom)
      (loc_in_room ?eloc ?eroom)
    )
    :effect (and
      (not (at ?sloc))
      (at ?eloc)
    )
  )

  (:action pick
    :parameters (?loc - location ?key - key ?room - room)
    :precondition (and
      (at ?loc)
      (key_at ?key ?loc)
      (key_for_room ?key ?room)
    )
    :effect (and (not (key_at ?key ?loc))
      (unlocked ?room)
    )
  )

)