(define (domain libraryworld)
    (:requirements :negative-preconditions :strips :typing)
    (:types book category)
    (:predicates (accessible ?x - book)  (belongs-to-category ?x - book ?cat - category)  (book-request ?book - book)  (checked-out ?book - book)  (hands-free) (holding ?x - book)  (on-shelf ?x - book ?y - book)  (on-table ?x - book)  (return-due ?book - book)  (shelf-empty ?cat - category)  (shelf-overflow ?cat - category))
    (:action check-out
        :parameters (?book - book)
        :precondition (and (accessible ?book) (not (checked-out ?book)))
        :effect (and (checked-out ?book))
    )
     (:action place-on-shelf
        :parameters (?x - book ?y - book)
        :precondition (and (holding ?x) (accessible ?y) (hands-free))
        :effect (and (not (holding ?x)) (on-shelf ?x ?y) (not (accessible ?y)) (accessible ?x) (hands-free))
    )
     (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and (not (holding ?book)) (hands-free) (on-table ?book) (accessible ?book))
    )
     (:action remove-from-shelf
        :parameters (?top-book - book ?bottom-book - book)
        :precondition (and (on-shelf ?top-book ?bottom-book) (accessible ?top-book) (hands-free))
        :effect (and (not (on-shelf ?top-book ?bottom-book)) (holding ?top-book) (accessible ?bottom-book))
    )
     (:action return-book
        :parameters (?book - book)
        :precondition (and (holding ?book) (return-due ?book))
        :effect (and (not (holding ?book)) (not (return-due ?book)))
    )
     (:action take-from-table
        :parameters (?x - book)
        :precondition (and (on-table ?x) (accessible ?x) (hands-free))
        :effect (and (not (on-table ?x)) (holding ?x))
    )
)