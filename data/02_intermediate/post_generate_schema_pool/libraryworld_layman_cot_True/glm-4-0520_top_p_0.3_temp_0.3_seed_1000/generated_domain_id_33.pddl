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
        :precondition (holding ?book)
        :effect (and
            (not (holding ?book))
            (accessible ?book)
            (on-table ?book)
        )
    )
    (:action place-on-shelf
        :parameters (?book-to-place - book ?book-underneath - book ?category - category)
        :precondition (and
            (holding ?book-to-place)
            (on-shelf ?book-underneath ?category)
            (accessible ?book-underneath)
            (belongs-to-category ?book-to-place ?category)
        )
        :effect (and
            (not (holding ?book-to-place))
            (on-shelf ?book-to-place ?category)
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
            (holding ?book)
            (accessible ?underneath)
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
            (checked-out ?book)
            (not (hands-free))
            (not (on-shelf ?book ?other-book)) ;; This assumes that the book is removed from the shelf
            (not (on-table ?book)) ;; This assumes that the book is removed from the table
        )
    )
    (:action return-book
        :parameters (?book - book)
        :precondition (holding ?book)
        :effect (not (checked-out ?book))
    )
)