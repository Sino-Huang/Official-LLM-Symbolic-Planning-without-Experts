
(define (problem organize-books)
	(:domain libraryworld)
	(:objects
		Book1 Book2 Book3 - book
		Fiction Non_Fiction Reference - category
	)
	(:init
		(on-table Book1)
		(on-shelf Book3 Book1)
		(on-table Book2)
		(accessible Book2)
		(accessible Book3)
		(hands-free)
		(belongs-to-category Book1 Fiction)
		(belongs-to-category Book2 Non_Fiction)
		(belongs-to-category Book3 Reference)
		(shelf-empty Fiction)
		(shelf-empty Non_Fiction)
		(shelf-empty Reference)
	)
	(:goal
		(and
			(on-shelf Book2 Book3)
			(on-shelf Book1 Book2)
		)
	)
)