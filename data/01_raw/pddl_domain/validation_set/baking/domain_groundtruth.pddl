(define (domain baking)
     (:requirements :strips :typing :negative-preconditions)
     (:types
          ingredient pan oven soap
     )
     (:predicates
          (is_egg ?egg - ingredient)
          (is_flour ?flour - ingredient)
          (pan_has_egg ?pan - pan)
          (pan_has_flour ?pan - pan)
          (pan_is_clean ?pan - pan)
          (pan_in_oven ?pan - pan)
          (in_pan ?x - ingredient ?pan - pan)
          (in_oven ?pan - pan ?oven - oven)
          (oven_is_full ?oven - oven)
          (hypothetical ?new - ingredient)
          (is_mixed ?pan - pan)
          (is_cake ?new - ingredient)
          (is_souffle ?new - ingredient)
          (soap_consumed ?soap - soap)

     )

     ; (:actions put_egg_in_pan put_flour_in_pan mix put_pan_in_oven remove_pan_from_oven bake_cake bake_souffle clean_pan)

     (:action put_egg_in_pan
          :parameters (?egg - ingredient ?pan - pan)
          :precondition (and
               (is_egg ?egg)
               (not (pan_has_egg ?pan))
               (not (is_mixed ?pan))
               (pan_is_clean ?pan)
               (not (pan_in_oven ?pan))
          )
          :effect (and (pan_has_egg ?pan)
               (in_pan ?egg ?pan)
          )
     )

     (:action put_flour_in_pan
          :parameters (?flour - ingredient ?pan - pan)
          :precondition (and
               (is_flour ?flour)
               (not (pan_has_flour ?pan))
               (not (is_mixed ?pan))
               (pan_is_clean ?pan)
               (not (pan_in_oven ?pan))
          )
          :effect (and (pan_has_flour ?pan)
               (in_pan ?flour ?pan)
          )
     )

     (:action mix
          :parameters (?egg - ingredient ?flour - ingredient ?pan - pan)
          :precondition (and
               (in_pan ?egg ?pan)
               (in_pan ?flour ?pan)
               (is_egg ?egg)
               (is_flour ?flour)
               (not (pan_in_oven ?pan))
          )
          :effect (and (is_mixed ?pan)
               (not (is_egg ?egg))
               (not (is_flour ?flour))
               (not (in_pan ?egg ?pan))
               (not (in_pan ?flour ?pan))
               (not (pan_has_egg ?pan))
               (not (pan_has_flour ?pan))
          )
     )

     (:action put_pan_in_oven
          :parameters (?pan - pan ?oven - oven)
          :precondition (and
               (not (oven_is_full ?oven))
               (not (pan_in_oven ?pan))
          )
          :effect (and (oven_is_full ?oven)
               (in_oven ?pan ?oven)
               (pan_in_oven ?pan)
          )
     )

     (:action remove_pan_from_oven
          :parameters (?pan - pan ?oven - oven)
          :precondition (and
               (in_oven ?pan ?oven)
          )
          :effect (and 
               (not (oven_is_full ?oven))
               (not (in_oven ?pan ?oven))
               (not (pan_in_oven ?pan))
          )
     )

     (:action bake_cake
          :parameters (?oven - oven ?pan - pan ?new - ingredient)
          :precondition (and
               (is_mixed ?pan)
               (in_oven ?pan ?oven)
               (hypothetical ?new)
          )
          :effect (and (not (is_mixed ?pan))
               (not (pan_is_clean ?pan))
               (not (hypothetical ?new))
               (is_cake ?new)
          )
     )

     (:action bake_souffle
          :parameters (?oven - oven ?egg - ingredient ?pan - pan ?new - ingredient)
          :precondition (and
               (in_pan ?egg ?pan)
               (is_egg ?egg)
               (not (pan_has_flour ?pan))
               (in_oven ?pan ?oven)
               (hypothetical ?new)
          )
          :effect (and 
               (not (is_egg ?egg))
               (not (in_pan ?egg ?pan))
               (not (pan_has_egg ?pan))
               (not (pan_is_clean ?pan))
               (not (hypothetical ?new))
               (is_souffle ?new)
          )
     )

     (:action clean_pan
          :parameters (?pan - pan ?soap - soap)
          :precondition (and
               (not (soap_consumed ?soap))
               (not (pan_in_oven ?pan))
          )
          :effect (and (pan_is_clean ?pan)
               (soap_consumed ?soap)
          )
     )

)