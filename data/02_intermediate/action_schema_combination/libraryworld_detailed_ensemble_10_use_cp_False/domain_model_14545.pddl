(define (domain libraryworld)
    (:requirements :negative-preconditions :strips :typing)
    (:types book category)
    (:predicates (accessible ?x - book)  (belongs-to-category ?x - book ?cat - category)  (book-request ?book - book)  (checked-out ?book - book)  (hands-free) (holding ?x - book)  (on-shelf ?x - book ?y - book)  (on-table ?x - book)  (return-due ?book - book)  (shelf-empty ?cat - category)  (shelf-overflow ?cat - category))
    (:action check-out
        :parameters (?book - book)
        :precondition (and (accessible ?book) (not (checked-out ?book)))
        :effect (and (not (accessible ?book)) (checked-out ?book) (return-due ?book))
    )
     (:action place-on-shelf
        :parameters (?x - book ?y - book)
        :precondition (and (holding ?x) (accessible ?y) (hands-free))
        :effect (and (not (holding ?x)) (on-shelf ?x ?y) (not (accessible ?y)) (accessible ?x) (hands-free))
    )
     (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and (not (holding ?book)) (on-table ?book) (accessible ?book) (hands-free))
    )
     (:action remove-from-shelf
        :parameters (?book - book ?supporting-book - book)
        :precondition (and (on-shelf ?book ?supporting-book) (accessible ?book) (hands-free))
        :effect (and (not (on-shelf ?book ?supporting-book)) (holding ?book) (accessible ?supporting-book))
    )
     (:action return-book
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and (not (holding ?book)) (not (return-due ?book)) (not (checked-out ?book)))
    )
     (:action take-from-table
        :parameters (?book - book)
        :precondition (and (on-table ?book) (accessible ?book) (hands-free))
        :effect (and (not (on-table ?book)) (holding ?book))
    )
)