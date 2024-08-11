(define (domain libraryworld)
    (:requirements :negative-preconditions :strips :typing)
    (:types book category)
    (:predicates (accessible ?x - book)  (belongs-to-category ?x - book ?cat - category)  (book-request ?book - book)  (checked-out ?book - book)  (hands-free) (holding ?x - book)  (on-shelf ?x - book ?y - book)  (on-table ?x - book)  (return-due ?book - book)  (shelf-empty ?cat - category)  (shelf-overflow ?cat - category))
    (:action check-out
        :parameters (?book - book)
        :precondition (and (accessible ?book) (hands-free) (not (checked-out ?book)))
        :effect (and (checked-out ?book))
    )
     (:action place-on-shelf
        :parameters (?x - book ?y - book)
        :precondition (and (holding ?x) (accessible ?y) (hands-free))
        :effect (and (on-shelf ?x ?y) (not (holding ?x)))
    )
     (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and (not (holding ?book)) (hands-free) (on-table ?book) (accessible ?book))
    )
     (:action remove-from-shelf
        :parameters (?book - book ?underneath_book - book ?category - category)
        :precondition (and (on-shelf ?book ?underneath_book) (accessible ?book) (hands-free))
        :effect (and (not (on-shelf ?book ?underneath_book)) (holding ?book) (accessible ?underneath_book))
    )
     (:action return-book
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and (not (checked-out ?book)))
    )
     (:action take-from-table
        :parameters (?book - book)
        :precondition (and (on-table ?book) (accessible ?book) (hands-free))
        :effect (and (not (on-table ?book)) (holding ?book))
    )
)