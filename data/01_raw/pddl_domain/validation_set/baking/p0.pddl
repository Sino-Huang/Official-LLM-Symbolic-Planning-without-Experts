(define (problem baking) 
    (:domain baking)

    (:objects
      oven-0 - oven
      egg-0 - ingredient
      flour-0 - ingredient
      soap-0 - soap
      pan-0 - pan
      new-0 - ingredient
    )

    (:init
    
    (is_egg egg-0)
    (is_flour flour-0)
    (hypothetical new-0)
    (pan_is_clean pan-0)

    )

    (:goal (and (is_cake new-0) ))
)