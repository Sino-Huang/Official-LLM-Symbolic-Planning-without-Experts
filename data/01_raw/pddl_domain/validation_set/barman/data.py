DOMAIN_DESC = "In this domain there is a robot barman that manipulates drink dispensers, glasses and a shaker. The goal is to find a plan of the robots actions that serves a desired set of drinks. In this domain deletes of actions encode relevant knowledge given that robot hands can only grasp one object at a time and given that glasses need to be empty and clean to be filled."

ACTION_DESC_DICT = {
    'clean-shaker' : {
        "detailed": "The robot cleans an empty shaker.",
        "layman": "Clean the empty shaker. The action is related to whether the shaker is empty and whether barman holds the shaker.",
    },
    'clean-shot' : {
        "detailed": "The robot cleans a used shot glass.",
        "layman": "clean the shot, it is depending on the conditions that whether the shot is empty and the precondition also need to know about whether barman holds the container.",
    },
    'empty-shaker' : {
        "detailed": "The robot empties a shaker that has been shaken, changing its level.",
        "layman": "Pour the contents out of the shaker. Things that are related to this action are whether the shaker is shacked or not, whether the shaker contains the cocktail or not and whether the shaker level goes back to empty level.",
    },
    'empty-shot' : {
        "detailed": "The robot empties a shot glass it's holding.",
        "layman": "empty the shot. It depends on whether the container has beverage and whether barman holds the container.",
    },
    'fill-shot' : {
        "detailed": "The robot fills an empty, clean shot glass with an ingredient from a dispenser.",
        "layman": "use a hand to hold a clean shot and fill ingredient that comes from the dispenser.",
    },
    'grasp' : {
        "detailed": "The robot uses a hand to pick up a container from the table.",
        "layman": "The action that barman is grasping is depending on the precondition that whether the container is in barman's hands or on the table.",
    },
    'leave' : {
        "detailed": "The robot places a container it's holding back onto the table.",
        "layman": "The action that barman is going to leave their container from his hand on to table.",
    },
    'pour-shaker-to-shot' : {
        "detailed": "The robot pours a beverage from a shaker into an empty, clean shot glass.",
        "layman": "Pour the shaken alcohol into a clean empty shot glass. The action is related to whether the shot is empty and clean, and whether the barman holds the shot and also it will affects the shaker level. ",
    },
    'pour-shot-to-clean-shaker' : {
        "detailed": "The robot pours an ingredient from a shot glass into a clean shaker, changing its level.",
        "layman": "Pour the hard liquor and other ingredients into a clean empty shaker and shake. The action is depending on the conditions that whether the shaker is empty and clean and also whether barman holds and shakes the shaker.",
    },
    'pour-shot-to-used-shaker' : {
        "detailed": "Similar to the previous action, but the shaker already contains ingredients and isn't clean.",
        "layman": "Pour the hard liquor and other ingredients into the used shaker. It depends on whether the barman start shaking or not. Also you need to hold the shot.",
    },
    'refill-shot' : {
        "detailed": "The robot refills a shot glass with the same ingredient it previously contained.",
        "layman": "refill the shot with the same ingredient. The action is depending on the conditions that whether the shot is empty and used and whether barman holds the shot.",
    },
    'shake' : {
        "detailed": "The robot shakes a shaker containing two ingredients to make a cocktail.",
        "layman": "make cocktail with two ingredients. The action that whether barman shakes the shaker is depending on the preconditions that whether the shaker has cocktail or ingredient and whether barman holds and shakes the shaker.",
    },
}

PREDICATE_DESC_LST = [
    '(ontable ?c - container) ;; the container is on the table',
    '(holding ?h - hand ?c - container) ;; the hand is holding the container',
    '(handempty ?h - hand) ;; the hand is empty',
    '(empty ?c - container) ;; the container is empty',
    '(contains ?c - container ?b - beverage) ;; the container contains the beverage',
    '(clean ?c - container) ;; the container is clean',
    '(used ?c - container ?b - beverage) ;; the container is used for the beverage',
    '(dispenses ?d - dispenser ?i - ingredient) ;; the dispenser dispenses the ingredient',
    '(shaker-empty-level ?s - shaker ?l - level) ;; the empty level of the shaker',
    '(shaker-level ?s - shaker ?l - level) ;; the shaker currently is at the level',
    '(next ?l1 ?l2 - level) ;; l2 is the next level after l1',
    '(unshaked ?s - shaker) ;; the shaker is unshaked',
    '(shaked ?s - shaker) ;; the shaker is shaked',
    '(cocktail-part1 ?c - cocktail ?i - ingredient) ;; the ingredient is part of the cocktail',
    '(cocktail-part2 ?c - cocktail ?i - ingredient) ;; the ingredient is part of the cocktail',
]