(define (problem minecraft) 
    (:domain minecraft)

    (:objects
    
    grass-0 - moveable
    grass-1 - moveable
    log-2 - moveable
    new-0 - moveable
    new-1 - moveable
    new-2 - moveable
    agent - agent
    loc-0-0 - static
    loc-0-1 - static
    loc-0-2 - static
    loc-0-3 - static
    loc-1-0 - static
    loc-1-1 - static
    loc-1-2 - static
    loc-1-3 - static
    loc-2-0 - static
    loc-2-1 - static
    loc-2-2 - static
    loc-2-3 - static
    loc-3-0 - static
    loc-3-1 - static
    loc-3-2 - static
    loc-3-3 - static
    )

    (:init
    
    (hypothetical new-0)
    (hypothetical new-1)
    (hypothetical new-2)
    (is_grass grass-0)
    (is_grass grass-1)
    (is_log log-2)
    (at grass-0 loc-2-2)
    (at grass-1 loc-0-0)
    (at log-2 loc-3-0)
    (agent_at loc-0-2)
    (handsfree agent)
    )

    ; action literals

    (:goal (and  (agent_at loc-1-1)  (inventory grass-1) ))
)
    