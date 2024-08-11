DOMAIN_DESC = "This domain is structured to allow navigation and interaction within a space comprising rooms, locations, and doors that can be unlocked with keys. The actions and predicates support movement between locations and the unlocking of rooms."

ACTION_DESC_DICT = {
    "move_to" : {
        "detailed": "The action is like embarking on a small journey from one place to another within a confined space. Imagine you're in a large house with multiple rooms. You're currently in one location, let's say the living room (your starting location). You decide to move to another spot, maybe the kitchen (your ending location). However, there's a catch. The kitchen is behind a door that needs to be unlocked (ending room). So, this action can only happen if the kitchen door is already unlocked. Once you move, you're no longer in the living room but now standing in the kitchen, contemplating what to cook!",
        "layman" : "Move from the s position to the e position and the room is not locked. I mean, the destination is inside an unlocked room. Otherwise you cannot go to that destination location",
    },
    "pick" : {
        "detailed": "This one is akin to a classic scene in adventure games where you find a key and use it to unlock new areas. Picture yourself in the same house. You find a key lying on a table in the hallway (the key's location). This isn't just any key; it's special because it opens the door to the mysterious attic (the room the key unlocks). By picking up this key, you perform the action. The moment you have the key in your hand, the attic is no longer inaccessible. It's as if the key magically signals the attic door to unlock, waiting for you to discover its secrets.",
        "layman" : "Retrieve the key from a certain location, picking the key means the room associated with that key turns unlocked.",
    },
}

PREDICATE_DESC_LST = [
    '(at ?loc - location) ;; agent is at loc location',
    '(unlocked ?room - room) ;; the room is unlocked',
    '(loc_in_room ?loc - location ?room - room) ;; the location is in the room',
    '(key_at ?key - key ?loc - location) ;; the key is at loc location',
    '(key_for_room ?key - key ?room - room) ;; the key is for the room',
]