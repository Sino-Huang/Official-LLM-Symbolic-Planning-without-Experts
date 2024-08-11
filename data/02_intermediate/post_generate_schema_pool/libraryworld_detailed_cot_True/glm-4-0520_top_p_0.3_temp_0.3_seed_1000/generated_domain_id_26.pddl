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
            (on-table ?book)
            (hands-free)
            (accessible ?book)
        )
    )
    (:action place-on-shelf
        :parameters (?book-hold - book ?book-shelf - book ?category - category)
        :precondition (and
            (holding ?book-hold)
            (on-shelf ?book-shelf)
            (accessible ?book-shelf)
            (belongs-to-category ?book-hold ?category)
        )
        :effect (and
            (not (holding ?book-hold))
            (hands-free)
            (on-shelf ?book-hold ?book-shelf)
            (not (accessible ?book-shelf))
            (accessible ?book-hold)
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?book-under - book)
        :precondition (and
            (on-shelf ?book ?book-under)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?book ?book-under))
            (holding ?book)
            (accessible ?book-under)
        )
    )
    (:action check-out
        :parameters (?book - book ?book - book)
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
            (not (return-due ?book))
            (not (checked-out ?book))
        )
    )
)