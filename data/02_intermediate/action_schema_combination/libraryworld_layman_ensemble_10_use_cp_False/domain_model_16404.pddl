(define (domain libraryworld)
    (:requirements :negative-preconditions :strips :typing)
    (:types book category)
    (:predicates (accessible ?x - book)  (belongs-to-category ?x - book ?cat - category)  (book-request ?book - book)  (checked-out ?book - book)  (hands-free) (holding ?x - book)  (on-shelf ?x - book ?y - book)  (on-table ?x - book)  (return-due ?book - book)  (shelf-empty ?cat - category)  (shelf-overflow ?cat - category))
    (:action check-out
        :parameters (?book - book)
        :precondition (and (accessible ?book) (not (checked-out ?book)))
        :effect (and (checked-out ?book) (not (on-shelf ?book ?book)) (not (on-table ?book)))
    )
     (:action place-on-shelf
        :parameters (?book-being-held - book ?book-on-shelf - book)
        :precondition (and (holding ?book-being-held) (accessible ?book-on-shelf))
        :effect (and (not (holding ?book-being-held)) (on-shelf ?book-being-held ?book-on-shelf))
    )
     (:action place-on-table
        :parameters (?book - book)
        :precondition (and (holding ?book) (hands-free))
        :effect (and (not (holding ?book)) (on-table ?book) (accessible ?book))
    )
     (:action remove-from-shelf
        :parameters (?book - book ?under_book - book)
        :precondition (and (on-shelf ?book ?under_book) (accessible ?book) (hands-free))
        :effect (and (not (on-shelf ?book ?under_book)) (holding ?book) (accessible ?under_book))
    )
     (:action return-book
        :parameters (?book - book)
        :precondition (and (holding ?book) (checked-out ?book))
        :effect (and (not (holding ?book)) (not (checked-out ?book)) (hands-free))
    )
     (:action take-from-table
        :parameters (?book - book)
        :precondition (and (on-table ?book) (accessible ?book) (hands-free))
        :effect (and (not (on-table ?book)) (holding ?book))
    )
)