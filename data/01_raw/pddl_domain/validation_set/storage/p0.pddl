; Map of the Depots:    
; * 
;-- 
; 0: depot0 area
; *: Depot access point
; =: Transit area

(define (problem storage-1)
(:domain storage)
(:objects
  depot0-1-1 container-0-0 - store_area
  hoist0 - hoist
  crate0 - crate
  container0 - container
  depot0 - depot
  loadarea - transit_area)

(:init
  (store_area_in depot0-1-1 depot0)
  (on crate0 container-0-0)
  (crate_in crate0 container0)
  (store_area_in container-0-0 container0)
  (connected loadarea container-0-0) 
  (connected container-0-0 loadarea)  
  (connected depot0-1-1 loadarea)
  (connected loadarea depot0-1-1)    
  (at hoist0 depot0-1-1)
  (available hoist0))

(:goal (and
  (crate_in crate0 depot0)))
)
