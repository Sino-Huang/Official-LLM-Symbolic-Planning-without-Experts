(define (domain libraryworld)
    (:requirements :negative-preconditions :strips :typing)
    (:types book category)
    (:predicates (accessible ?x - book)  (belongs-to-category ?x - book ?cat - category)  (book-request ?book - book)  (checked-out ?book - book)  (hands-free) (holding ?x - book)  (on-shelf ?x - book ?y - book)  (on-table ?x - book)  (return-due ?book - book)  (shelf-empty ?cat - category)  (shelf-overflow ?cat - category))
    (:action check-out
        :parameters (?book - book)
        :precondition (and (accessible ?book) (hands-free) (not (checked-out ?book)))
        :effect (and (not (accessible ?book)) (checked-out ?book))
    )
     (:action place-on-shelf
        :parameters (?book - book ?target-book - book)
        :precondition (and (holding ?book) (accessible ?target-book))
        :effect (and (not (holding ?book)) (on-shelf ?book ?target-book) (hands-free))
    )
     (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and (not (holding ?book)) (on-table ?book) (accessible ?book) (hands-free))
    )
     (:action remove-from-shelf
        :parameters (?book - book ?under_book - book)
        :precondition (and (on-shelf ?book ?under_book) (accessible ?book) (hands-free))
        :effect (and (not (on-shelf ?book ?under_book)) (holding ?book) (accessible ?under_book))
    )
     (:action return-book
        :parameters (?book - book)
        :precondition (and (holding ?book) (checked-out ?book))
        :effect (and (not (checked-out ?book)) (accessible ?book) (hands-free))
    )
     (:action take-from-table
        :parameters (?book - book)
        :precondition (and (on-table ?book) (accessible ?book) (hands-free))
        :effect (and (not (on-table ?book)) (not (hands-free)) (holding ?book))
    )
)