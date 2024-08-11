(define (domain libraryworld)
	 (:requirements :strips :typing :negative-preconditions)
	 
	 (:types book category)
	 
	 (:predicates
	   (on-shelf ?x ?y - book)
	   (on-table ?x - book)
	   (accessible ?x - book)
	   (hands-free)
	   (holding ?x - book)
	   (belongs-to-category ?x - book ?cat - category)
	   (shelf-empty ?shelf - category)
	   (shelf-overflow ?shelf - category)
	   (book-request ?book - book)
	   (return-due ?book - book)
	   (checked-out ?book - book)
	 )
	 
	 (:action take-from-table
	   :parameters (?x - book)
	   :precondition (and (accessible ?x) (on-table ?x) (hands-free))
	   :effect (and (not (on-table ?x))
	                (not (accessible ?x))
	                (not (hands-free))
	                (holding ?x))
	 )
	 
	 (:action place-on-table
	   :parameters (?x - book)
	   :precondition (holding ?x)
	   :effect (and (not (holding ?x))
	                (accessible ?x)
	                (hands-free)
	                (on-table ?x))
	 )
	 
	 (:action place-on-shelf
	   :parameters (?x ?y - book ?cat - category)
	   :precondition (and (holding ?x) (accessible ?y) (belongs-to-category ?x ?cat) (not (shelf-overflow ?cat)))
	   :effect (and (not (holding ?x))
	                (not (accessible ?y))
	                (accessible ?x)
	                (hands-free)
	                (on-shelf ?x ?y)
	                (shelf-empty ?cat))
	 )
	 
	 (:action remove-from-shelf
	   :parameters (?x ?y - book ?cat - category)
	   :precondition (and (on-shelf ?x ?y) (accessible ?x) (hands-free) (belongs-to-category ?x ?cat))
	   :effect (and (holding ?x)
	                (accessible ?y)
	                (not (accessible ?x))
	                (not (hands-free))
	                (not (on-shelf ?x ?y))
	                (shelf-empty ?cat))
	 )
	 
	 (:action check-out
	   :parameters (?x - book)
	   :precondition (and (accessible ?x) (not (checked-out ?x)))
	   :effect (and (checked-out ?x)
	                (not (accessible ?x))
	                (book-request ?x)
	                (return-due ?x))
	 )
	 
	 (:action return-book
	   :parameters (?x - book)
	   :precondition (and (checked-out ?x) (holding ?x))
	   :effect (and (not (checked-out ?x))
	                (not (holding ?x))
	                (not (book-request ?x))
	                (not (return-due ?x))
	                (accessible ?x)
	                (hands-free))
	 )
	)