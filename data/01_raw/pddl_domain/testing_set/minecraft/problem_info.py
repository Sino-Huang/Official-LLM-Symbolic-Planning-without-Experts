INIT_STATE_DESC = "In the Minecraft world, there are several moveable objects: grass-0, grass-1, log-2, new-0, new-1, and new-2. The agent is positioned at location loc-0-2 and currently has free hands. The hypothetical objects new-0, new-1, and new-2 exist but are not yet tangible in the environment. Grass-0 is located at loc-2-2, grass-1 is at loc-0-0, and log-2 is at loc-3-0. The agent can interact with these objects and move between various static locations, which include loc-0-0 through loc-3-3."



GOAL_STATE_DESC = "The objective is for the agent to be positioned at location loc-1-1 and to have grass-1 in its inventory."

OBJECT_SNIPPET_STR = """(:objects
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
"""