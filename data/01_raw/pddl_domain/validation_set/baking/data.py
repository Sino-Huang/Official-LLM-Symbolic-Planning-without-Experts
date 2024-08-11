DOMAIN_DESC = "This describes a cooking or baking process where ingredients such as eggs and flour are used. The process of baking involves putting eggs in the pan followed by the flour, mix the two and then put the pan in the oven and then remove the pan from the oven to get the baked cake. Lastly, the pan is cleaned using a soap. Well, you can also bake a souffle but in at bit different process."

ACTION_DESC_DICT = {
    "bake_cake" : {
        "detailed": "Baking a cake involves transforming mixed ingredients in a pan into a cake. This action is possible when the ingredients in the pan are mixed, the pan is in the oven, and it involves creating a new type of ingredient, termed here as hypothetical. The end result is a cake, and the pan becomes dirty.",
        "layman": "A new hypothetical ingredient is used to bake a cake, now the new ingredient becomes a cake."
    },
    "bake_souffle": {
        "detailed": "This action represents the process of making a souffle. It requires an egg in a pan (without flour), with the pan placed in an oven. A new, hypothetical ingredient is involved, which becomes a souffle as a result of this process. After baking, the pan is no longer clean.",
        "layman": "a new hypothetical ingredient is used to bake a souffle. baking souffle needs eggs, oven, a pan and other new ingredients. The pan with eggs and other ingredients excludes flour is put in oven which is not full. Then get a souffle.",
    },
    "clean_pan": {
        "detailed": "Cleaning a pan is the process of making a used pan clean again with the help of soap. It's possible only when the pan is not in the oven, and there is soap available to use. After cleaning, the pan is clean, and the soap is considered used up.",
        "layman": "Action cleaning pan needs a pan and soap. Use soap to clean a pan which is not in the oven. Then get a clean pan.",
    },
    "mix": {
        "detailed": "Mixing is the process of combining the egg and flour in a pan. This action is feasible when both egg and flour are in the pan, and they haven't been mixed yet. The pan should not be in the oven during this process. After mixing, the egg and flour lose their individual identities.",
        "layman": "Action mixing needs eggs, flour and a pan. The pan has mixed stuff in it.",
    },
    "put_egg_in_pan": {
        "detailed": "This action involves placing an egg into a pan. It's only possible when the pan is clean, not already in the oven, does not contain an egg, and the ingredients in it are not yet mixed.",
        "layman": "Action putting the eggs in the pan needs eggs and a pan. The clean pan now has an egg in it.",
    },
    "put_flour_in_pan": {
        "detailed": "This action is about adding flour to a pan. It can be done when the pan is clean, not in the oven, doesn't have flour in it already, and the contents of the pan haven't been mixed.",
        "layman": "Action putting the flour in the pan needs flour and a pan. The clean pan now has flour in it.",
    },
    "put_pan_in_oven": {
        "detailed": "This action involves placing a pan inside an oven. It is only possible if the oven isn't already full and the pan isn't in the oven. When the pan is placed in the oven, the oven becomes full.",
        "layman": "Action putting pan in oven needs oven and a pan. The pan is put in oven which is not full.",
    },
    "remove_pan_from_oven": {
        "detailed": "This action is about taking a pan out of the oven. It can only be done if the pan is actually in the oven. Once the pan is removed, the oven is no longer considered full.",
        "layman": "Action removing pan from oven needs oven and a pan. Then the pan is not in oven. ",        
    },
}

PREDICATE_DESC_LST = [
    '(is_egg ?egg - ingredient) ;; the ingredient is an egg',
    '(is_flour ?flour - ingredient) ;; the ingredient is flour',
    '(pan_has_egg ?pan - pan) ;; the pan has an egg',
    '(pan_has_flour ?pan - pan) ;; the pan has flour',
    '(pan_is_clean ?pan - pan) ;; the pan is clean',
    '(pan_in_oven ?pan - pan) ;; the pan is in the oven',
    '(in_pan ?x - ingredient ?pan - pan) ;; the ingredient is in the pan',
    '(in_oven ?pan - pan ?oven - oven) ;; the pan is in the oven',
    '(oven_is_full ?oven - oven) ;; the oven is full',
    '(hypothetical ?new - ingredient) ;; the ingredient is hypothetical',
    '(is_mixed ?pan - pan) ;; the ingredients in the pan are mixed',
    '(is_cake ?new - ingredient) ;; the ingredient is a cake',
    '(is_souffle ?new - ingredient) ;; the ingredient is a souffle',
    '(soap_consumed ?soap - soap) ;; the soap is consumed',
]