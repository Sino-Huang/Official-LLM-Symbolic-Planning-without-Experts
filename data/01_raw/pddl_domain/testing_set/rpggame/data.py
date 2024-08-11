DOMAIN_DESC = "Help the hero to get out of dungeon! A hero woke up in a dungeon full of monsters and traps (perhaps the party last night went wrong...) and needs your help to get out.  Here are basic facts for the dungeon domain: - The dungeon contains rooms that are **connected** by corridors (dungeon can thus be represented by undirected graph) - each room can be **empty**, or can have a **monster** in it, or can have a **trap** in it, or can have a **sword** in it - one of the empty rooms is the **goal**: it has an exit, so the hero can escape"



ACTION_DESC_DICT = {
    'move' : {
        "detailed": "The hero can **move** to an adjacent room (connected by a corridor) that has not been destroyed (i.e., the hero has not already visited the room). When this action is executed, the original cell get destroyed.",
        "layman": "Hero can move if the - hero is at current location - cells are connected, - there is no trap in current loc, and - destination does not have a trap/monster.",
    },
    'move-to-trap' : {
        "detailed": "The hero can **move** to an adjacent room (connected by a corridor) that has not been destroyed (i.e., the hero has not already visited the room). When this action is executed, the hero gets into a location with a trap",
        "layman": "Hero can move if the - hero is at current location - cells are connected, - when this action is executed, the hero gets into a location with a trap",
    },
    'move-to-monster' : {
        "detailed": "The hero can **move** to an adjacent room (connected by a corridor) that has not been destroyed (i.e., the hero has not already visited the room). When this action is executed, the hero gets into a location with a monster",
        "layman": "Hero can move if the - hero is at current location - cells are connected, - when this action is executed, the hero gets into a location with a monster",
    },
    'pick-sword' : {
        "detailed": "**Pickup** the sword if present in the room the hero is currently in and the hero is empty handed",
        "layman": "Hero picks a sword if he's in the same location",
    },
    'destroy-sword' : {
        "detailed": "**Destroy** the sword that the hero currently holds. However, this can have unpleasant effects if done in a room with a monster: it invites the monster to eat the hero.",
        "layman": "Hero's destroys his sword. So that he is arm-free and can disarm traps in the future if required. ",
    },
    'disarm-trap' : {
        "detailed": "**Disarm a trap** – if there is a trap in the room the hero is in and the hero is empty-handed (does not hold a sword), then the hero can disarm it",
        "layman": "Hero's disarm the trap with his hand. Make sure the hand is free.",
    },
}

PREDICATE_DESC_LST = [
    "(at-hero ?loc - cells) ;;  Hero's cell location",
    "(at-sword ?s - swords ?loc - cells) ;; Sword cell location",
    "(has-monster ?loc - cells) ;; Indicates if a cell location has a monster",
    "(has-trap ?loc - cells) ;; Indicates if a cell location has a trap",
    "(is-destroyed ?obj) ;; Indicates if a chell or sword has been destroyed",
    "(connected ?from ?to - cells) ;; connects cells",
    "(arm-free) ;; Hero's hand is free",
    "(holding ?s - swords) ;; Hero's holding a sword",
    "(trap-disarmed ?loc) ;; It becomes true when a trap is disarmed",
]


TYPE_INFO_STR = """(:types
    swords cells
)"""