DOMAIN_DESC = "This domain is structured to model a simple newspaper delivery system, where the main tasks involve picking up newspapers from a home base, moving to different locations, and delivering the papers to locations that require them."

ACTION_DESC_DICT = {
    "deliver" : {
        "detailed": """The house at loc_house1 wants a newspaper.
RoboDelivery performs the deliver action to give paper1 to the house.

    Preconditions: RoboDelivery is at loc_house1, the house wants a newspaper, and RoboDelivery is carrying paper1.
    Effects: RoboDelivery is no longer carrying paper1, the house at loc_house1 no longer wants a newspaper, and the house at loc_house1 is satisfied.""",
        "layman": "Deliver the newspaper to the location",
    },
    "move" : {
        "detailed": """RoboDelivery wants to deliver the newspaper to a house (loc_house1).
RoboDelivery performs the move action to go from loc_home to loc_house1.

    Preconditions: RoboDelivery is at loc_home.
    Effects: RoboDelivery is no longer at loc_home and is now at loc_house1.""",
        "layman": "Move from one location to another location",
    },
    "pick-up" : {
        "detailed": """RoboDelivery is at the home base (loc_home).
There is an unpacked newspaper (paper1) at the home base.
RoboDelivery performs the pick-up action.

    Preconditions: RoboDelivery is at loc_home (which is the home base), and paper1 is unpacked.
    Effects: RoboDelivery is now carrying paper1, and paper1 is no longer unpacked.""",
        "layman": "Pick up the newspaper from a certain location",
    },
}

PREDICATE_DESC_LST = [
    "(at ?loc - loc) ;; the agent is at loc location",
    "(is_Home_Base ?loc - loc) ;; the location is the home base",
    "(satisfied ?loc - loc) ;; the location has received the newspaper",
    "(wants_Paper ?loc - loc) ;; the location needs a newspaper",
    "(unpacked ?paper - paper) ;; the paper is unpacked",
    "(carrying ?paper - paper) ;; the agent is carrying the paper",
]