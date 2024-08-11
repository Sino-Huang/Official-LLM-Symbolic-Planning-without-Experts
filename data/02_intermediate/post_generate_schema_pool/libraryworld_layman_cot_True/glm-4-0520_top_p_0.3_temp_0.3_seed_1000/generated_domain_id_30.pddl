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
            (hands-free)
        )
        :effect (and
            (not (holding ?book))
            (on-table ?book)
            (accessible ?book)
        )
    )
    (:action place-on-shelf
        :parameters (?book - book ?target-book - book)
        :precondition (and
            (hands-free)
            (holding ?book)
            (on-shelf ?target-book)
            (accessible ?target-book)
        )
        :effect (and
            (not (holding ?book))
            (not (hands-free))
            (on-shelf ?book ?target-book)
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?underneath-book - book)
        :precondition (and
            (hands-free)
            (on-shelf ?book ?underneath-book)
            (accessible ?book)
        )
        :effect (and
            (not (on-shelf ?book ?underneath-book))
            (holding ?book)
            (accessible ?underneath-book)
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