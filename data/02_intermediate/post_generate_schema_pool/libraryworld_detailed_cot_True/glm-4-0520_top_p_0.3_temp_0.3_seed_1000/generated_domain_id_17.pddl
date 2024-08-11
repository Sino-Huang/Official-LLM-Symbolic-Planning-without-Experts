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
        :parameters (?x - book)
        :precondition (and
            (on-table ?x)
            (accessible ?x)
            (hands-free)
        )
        :effect (and
            (not (on-table ?x))
            (holding ?x)
        )
    )
    (:action place-on-table
        :parameters (?book - book)
        :precondition (and
            (holding ?book)
        )
        :effect (and
            (not (holding ?book))
            (on-table ?book)
            (accessible ?book)
            (hands-free)
        )
    )
    (:action place-on-shelf
        :parameters (?book - book ?below-book - book)
        :precondition (and
            (holding ?book)
            (on-shelf ?below-book ?book)
            (accessible ?below-book)
        )
        :effect (and
            (not (holding ?book))
            (on-shelf ?book ?below-book)
            (not (accessible ?below-book))
            (hands-free)
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
            (accessible ?bottom-book)
        )
    )
    (:action check-out
        :parameters (?book - book)
        :precondition (and
            (accessible ?book)
            (not (checked-out ?book))
        )
        :effect (and
            (not (accessible ?book))
            (checked-out ?book)
            ;(return-due ?book) ; This would be an effect if we were to include setting the due date in this action.
        )
    )
    (:action return-book
        :parameters (?book - book)
        :precondition (and
            (holding ?book)
            (return-due ?book)
        )
        :effect (and
            (not (checked-out ?book))
            (not (return-due ?book))
            (hands-free)
            (on-table ?book)
        )
    )
)