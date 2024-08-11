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
            (not (hands-free))
            (holding ?x)
        )
    )
    (:action place-on-table
        :parameters (?b - book)
        :precondition (and
            (holding ?b)
            (accessible ?b)
        )
        :effect (and
            (not (holding ?b))
            (on-table ?b)
            (accessible ?b)
        )
    )
    (:action place-on-shelf
        :parameters (?book - book ?below-book - book)
        :precondition (and
            (holding ?book)
            (on-shelf ?below-book)
            (accessible ?below-book)
        )
        :effect (and
            (not (holding ?book))
            (not (accessible ?below-book))
            (on-shelf ?book ?below-book)
            (accessible ?book)
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
            (accessible ?bottom-book)
            (holding ?top-book)
            (not (hands-free))
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
            (not (checked-out ?book))
            (not (return-due ?book))
        )
    )
)