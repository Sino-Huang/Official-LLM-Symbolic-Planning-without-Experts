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
        :parameters (?x - book)
        :precondition (and
            (holding ?x)
        )
        :effect (and
            (not (holding ?x))
            (on-table ?x)
            (accessible ?x)
            (hands-free)
        )
    )
    (:action place-on-shelf
        :parameters (?x - book ?y - book)
        :precondition (and
            (holding ?x)
            (on-shelf ?y)
            (accessible ?y)
        )
        :effect (and
            (not (holding ?x))
            (on-shelf ?x ?y)
            (not (accessible ?y))
            (hands-free)
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?underneath - book)
        :precondition (and
            (on-shelf ?book ?underneath)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?book ?underneath))
            (accessible ?underneath)
            (holding ?book)
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
            (return-due ?book)
        )
        :effect (and
            (not (checked-out ?book))
            (not (return-due ?book))
        )
    )
)