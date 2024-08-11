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
        :precondition (and
            (holding ?book)
        )
        :effect (and
            (not (holding ?book))
            (accessible ?book)
        )
    )
    (:action place-on-shelf
        :parameters (?held-book - book ?shelf-book - book)
        :precondition (and
            (holding ?held-book)
            (on-shelf ?shelf-book)
            (accessible ?shelf-book)
        )
        :effect (and
            (not (holding ?held-book))
            (not (accessible ?shelf-book))
            (on-shelf ?held-book ?shelf-book)
            (hands-free)
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?supporting_book - book)
        :precondition (and
            (on-shelf ?book ?supporting_book)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?book ?supporting_book))
            (holding ?book)
            (accessible ?supporting_book)
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
            (not (checked-out ?book))
            (not (return-due ?book))
        )
    )
)