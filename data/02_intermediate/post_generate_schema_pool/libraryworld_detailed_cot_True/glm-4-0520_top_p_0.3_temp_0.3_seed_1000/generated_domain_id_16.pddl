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
            (not (hands-free))
        )
    )
    (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and
            (not (holding ?book))
            (accessible ?book)
            (hands-free)
        )
    )
    (:action place-on-shelf
        :parameters (?book - book ?book-on-shelf - book)
        :precondition (and
            (holding ?book)
            (on-shelf ?book-on-shelf)
            (accessible ?book-on-shelf)
        )
        :effect (and
            (not (holding ?book))
            (on-shelf ?book ?book-on-shelf)
            (not (accessible ?book-on-shelf))
            (accessible ?book)
            (hands-free)
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?supporting-book - book ?category - category)
        :precondition (and
            (on-shelf ?book ?supporting-book)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?book ?supporting-book))
            (accessible ?supporting-book)
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
            (hands-free)
        )
        :effect (and
            (not (holding ?book))
            (not (return-due ?book))
        )
    )
)