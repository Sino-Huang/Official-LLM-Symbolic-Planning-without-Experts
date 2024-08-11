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
        :parameters (?x - book)
        :precondition (and
            (holding ?x)
        )
        :effect (and
            (on-table ?x)
            (accessible ?x)
            (hands-free)
        )
    )
    (:action place-on-shelf
        :parameters (?book-h - book ?book-s - book)
        :precondition (and
            (holding ?book-h)
            (on-shelf ?book-s)
            (accessible ?book-s)
        )
        :effect (and
            (not (holding ?book-h))
            (on-shelf ?book-h ?book-s)
            (accessible ?book-h)
        )
    )
    (:action remove-from-shelf
        :parameters (?x - book ?y - book)
        :precondition (and
            (hands-free)
            (accessible ?x)
            (on-shelf ?x ?y)
        )
        :effect (and
            (not (hands-free))
            (holding ?x)
            (not (on-shelf ?x ?y))
            (accessible ?y)
        )
    )
    (:action check-out
        :parameters (?book - book)
        :precondition (and
            (accessible ?book)
            (hands-free)
            (not (checked-out ?book))
        )
        :effect (and
            (not (on-shelf ?book ?y))
            (not (on-table ?book))
            (checked-out ?book)
        )
    )
    (:action return-book
        :parameters (?book - book)
        :precondition (and
            (holding ?book)
        )
        :effect (and
            (not (checked-out ?book))
        )
    )
)