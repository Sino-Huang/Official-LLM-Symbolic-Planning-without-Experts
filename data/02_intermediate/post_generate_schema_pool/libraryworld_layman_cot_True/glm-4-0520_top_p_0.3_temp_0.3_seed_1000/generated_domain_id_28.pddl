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
        :parameters (?b - book)
        :precondition (and
            (on-table ?b)
            (accessible ?b)
            (hands-free)
        )
        :effect (and
            (not (on-table ?b))
            (holding ?b)
            (not (hands-free))
        )
    )
    (:action place-on-table
        :parameters (?book - book)
        :precondition (and
            (holding ?book)
        )
        :effect (and
            (not (holding ?book))
            (accessible ?book)
            (on-table ?book)
        )
    )
    (:action place-on-shelf
        :parameters (?book - book ?below-book - book)
        :precondition (and
            (holding ?book)
            (on-shelf ?below-book)
            (accessible ?below-book)
            (hands-free)
        )
        :effect (and
            (not (holding ?book))
            (on-shelf ?book ?below-book)
            (accessible ?book)
        )
    )
    (:action remove-from-shelf
        :parameters (?b1 - book ?b2 - book)
        :precondition (and
            (hands-free)
            (on-shelf ?b1 ?b2)
            (accessible ?b1)
        )
        :effect (and
            (not (on-shelf ?b1 ?b2))
            (holding ?b1)
            (accessible ?b2)
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
            (not (accessible ?book))
            (checked-out ?book)
        )
    )
    (:action return-book
        :parameters (?book - book)
        :precondition (and
            (holding ?book)
            (return-due ?book)
        )
        :effect (and
            (not (return-due ?book))
            (not (checked-out ?book))
        )
    )
)