(define (domain libraryworld)

    (:requirements :strips :typing :negative-preconditions)

    (:types book category)

    (:predicates
        (on-shelf ?x ?y - book) ;; ?x is on top of ?y on the shelf
        (on-table ?x - book) ;; ?x is on the table
        (accessible ?x - book) ;; ?x is accessible (not covered)
        (hands-free) ;; The hands of the librarian are free
        (holding ?x - book) ;; The librarian is holding ?x
        (belongs-to-category ?x - book ?cat - category) ;; ?x belongs to the category ?cat
        (shelf-empty ?cat - category) ;; The shelf for category ?cat is empty
        (shelf-overflow ?cat - category) ;; The shelf for category ?cat is full
        (book-request ?book - book) ;; There is a request for book ?book
        (return-due ?book - book) ;; Book ?book is due for return
        (checked-out ?book - book) ;; Book ?book is checked out
    )

    (:action take-from-table
        :parameters (?book - book)
        :precondition (and
            (on-table ?book)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-table ?book))
            (not (hands-free))
            (holding ?book)
        )
    )
    (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and
            (not (holding ?book))
            (on-table ?book)
            (hands-free)
            (accessible ?book)
        )
    )
    (:action place-on-shelf
        :parameters (?book - book ?below - book)
        :precondition (and
            (holding ?book)
            (accessible ?below)
            (belongs-to-category ?book ?cat)
            (belongs-to-category ?below ?cat)
            (not (on-shelf ?book ?below))
        )
        :effect (and
            (not (holding ?book))
            (on-shelf ?book ?below)
            (accessible ?book)
            (not (accessible ?below))
        )
    )
    (:action remove-from-shelf
        :parameters (?top-book - book ?bottom-book - book)
        :precondition (and
            (on-shelf ?top-book ?bottom-book)
            (accessible ?top-book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?top-book ?bottom-book))
            (holding ?top-book)
            (not (hands-free))
            (accessible ?bottom-book)
        )
    )
    (:action check-out
        :parameters (?book - book)
        :precondition (and
            (accessible ?book)
            (not (checked-out ?book))
            (hands-free)
        )
        :effect (and
            (checked-out ?book)
            (return-due ?book)
        )
    )
    (:action return-book
        :parameters (?book - book)
        :precondition (and
            (holding ?book)
            (return-due ?book)
        )
        :effect (and
            (not (holding ?book))
            (not (return-due ?book))
        )
    )
)