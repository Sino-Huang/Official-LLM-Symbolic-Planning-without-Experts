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
        :parameters (?book - book ?category - category)
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
        )
    )
    (:action place-on-shelf
        :parameters (?book-held - book ?book-on-shelf - book)
        :precondition (and
            (holding ?book-held)
            (on-shelf ?book-on-shelf)
            (accessible ?book-on-shelf)
            (hands-free)
        )
        :effect (and
            (not (holding ?book-held))
            (on-shelf ?book-held)
            (not (accessible ?book-on-shelf)) ; This may be omitted if the rules allow the underlying book to remain accessible
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?underbook - book)
        :precondition (and
            (on-shelf ?book ?underbook)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?book ?underbook))
            (holding ?book)
            (accessible ?underbook)
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
            (not (accessible ?book))
            (checked-out ?book)
        )
    )
    (:action return-book
        :parameters (?book - book)
        :precondition (and
            (holding ?book)
            (checked-out ?book)
        )
        :effect (and
            (not (holding ?book))
            (not (checked-out ?book))
            (hands-free)
        )
    )
)