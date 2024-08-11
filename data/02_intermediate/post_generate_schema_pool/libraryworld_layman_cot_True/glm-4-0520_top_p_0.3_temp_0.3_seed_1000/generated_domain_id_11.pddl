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
            (not (accessible ?book))
            (holding ?book)
        )
    )
    (:action place-on-table
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (and
            (not (holding ?book))
            (hands-free)
            (on-table ?book)
            (accessible ?book)
        )
    )
    (:action place-on-shelf
        :parameters (?book - book ?other-book - book)
        :precondition (and
            (holding ?book)
            (on-shelf ?other-book)
            (accessible ?other-book)
            (hands-free)
        )
        :effect (and
            (not (holding ?book))
            (on-shelf ?book ?other-book)
        )
    )
    (:action remove-from-shelf
        :parameters (?book - book ?underneath_book - book)
        :precondition (and
            (on-shelf ?book ?underneath_book)
            (accessible ?book)
            (hands-free)
        )
        :effect (and
            (not (on-shelf ?book ?underneath_book))
            (holding ?book)
            (not (hands-free))
            (accessible ?underneath_book)
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
        :parameters (?book - book ?category - category)
        :precondition (and
            (book-request ?book)
            (checked-out ?book)
            (belongs-to-category ?book ?category)
        )
        :effect (and
            (not (checked-out ?book))
            (available ?book)
            (not (book-request ?book))
            (shelf-empty ?category)
        )
    )
)