(define (domain libraryworld)
    (:requirements :negative-preconditions :strips :typing)
    (:types book category)
    (:predicates (accessible ?x - book)  (belongs-to-category ?x - book ?cat - category)  (book-request ?book - book)  (checked-out ?book - book)  (hands-free) (holding ?x - book)  (on-shelf ?x - book ?y - book)  (on-table ?x - book)  (return-due ?book - book)  (shelf-empty ?cat - category)  (shelf-overflow ?cat - category))
    (:action check-out
        :parameters (?book - book)
        :precondition (and (accessible ?book) (hands-free) (not (checked-out ?book)))
        :effect (and (not (accessible ?book)) (holding ?book) (checked-out ?book))
    )
     (:action place-on-shelf
        :parameters (?book-being-held - book ?book-on-shelf - book)
        :precondition (and (holding ?book-being-held) (accessible ?book-on-shelf))
        :effect (and (not (holding ?book-being-held)) (on-shelf ?book-being-held ?book-on-shelf))
    )
     (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and (not (holding ?book)) (hands-free) (on-table ?book) (accessible ?book))
    )
     (:action remove-from-shelf
        :parameters (?x - book ?y - book)
        :precondition (and (hands-free) (on-shelf ?x ?y) (accessible ?x))
        :effect (and (not (on-shelf ?x ?y)) (holding ?x) (accessible ?y))
    )
     (:action return-book
        :parameters (?book - book)
        :precondition (and (holding ?book) (checked-out ?book))
        :effect (and (not (checked-out ?book)) (accessible ?book) (hands-free))
    )
     (:action take-from-table
        :parameters (?x - book)
        :precondition (and (on-table ?x) (accessible ?x) (hands-free))
        :effect (and (not (on-table ?x)) (not (hands-free)) (holding ?x))
    )
)