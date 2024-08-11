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
            (holding ?book)
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
        :parameters (?held-book - book ?base-book - book)
        :precondition (and
            (holding ?held-book)
            (on-shelf ?base-book)
            (accessible ?base-book)
        )
        :effect (and
            (not (holding ?held-book))
            (not (accessible ?base-book))
            (on-shelf ?held-book)
            (hands-free)
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?under_book - book ?category - category)
        :precondition (and
            (on-shelf ?book ?under_book)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?book ?under_book))
            (holding ?book)
            (accessible ?under_book)
        )
    )
    (:action check-out
        :parameters (?book - book)
        :precondition (and
            (accessible ?book)
            (not (checked-out ?book))
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
        )
        :effect (and
            (not (holding ?book))
            (not (return-due ?book))
            (not (checked-out ?book))
        )
    )
)