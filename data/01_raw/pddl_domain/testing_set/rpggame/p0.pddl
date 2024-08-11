;Network plugin with input below
;1 2 3 4 5
;6 7 8 5
;2 6
;3 7
;4 8

(define (problem p1-dangeon)
  (:domain rpggame)
  (:objects
            cell1 cell2 cell3 cell4 cell5 cell6 cell7 cell8 - cells
            sword1 - swords
  )
  (:init
  
    ;Initial Hero Location
    (at-hero cell5)
    
    ;He starts with a free arm
    (arm-free)
    
    ;Initial location of the swords
    (at-sword sword1 cell4)
    
    ;Initial location of Monsters
    (has-monster cell3)
    (has-monster cell8)
    
    ;Initial lcocation of Traps
    (has-trap cell2)
    
    ;Graph Connectivity
    (connected cell1 cell2)
    (connected cell2 cell1)
    (connected cell2 cell3)
    (connected cell3 cell2)
    (connected cell3 cell4)
    (connected cell4 cell3)
    (connected cell4 cell5)
    (connected cell5 cell4)
    (connected cell6 cell7)
    (connected cell7 cell6)
    (connected cell7 cell8)
    (connected cell8 cell7)
    (connected cell8 cell5)
    (connected cell5 cell8)
    (connected cell2 cell6)
    (connected cell6 cell2)
    (connected cell3 cell7)
    (connected cell7 cell3)
    (connected cell4 cell8)
    (connected cell8 cell4)
  )
  (:goal (and
            ;Hero's Goal Location
            (at-hero cell1)
  ))
  
)
