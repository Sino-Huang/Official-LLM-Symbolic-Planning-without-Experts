DOMAIN_DESC = "This domain is to plan how to make and serve sandwiches for a group of children in which some are allergic to gluten. There are two actions for making sandwiches from their ingredients. The first one makes a sandwich and the second one makes a sandwich taking into account that all ingredients are gluten-free. There are also actions to put a sandwich on a tray and to serve sandwiches. Problems in this domain define the ingredients to make sandwiches at the initial state. Goals consist of having all kids served with a sandwich to which they are not allergic."

ACTION_DESC_DICT = {
    "make_sandwich" : {
        "detailed": "Creates a sandwich using bread and content portions. Removes the bread and content portions from the kitchen and adds the sandwich to the kitchen.",
        "layman": "Make a sandwich using the bread and fillings available in the kitchen. The action will use up the bread and content. ",
    },
    "make_sandwich_no_gluten" : {
        "detailed": "Creates a gluten-free sandwich using gluten-free bread and content portions. Removes the bread and content portions from the kitchen and adds the gluten-free sandwich to the kitchen.",
        "layman": "Select gluten-free ingredients from the existing bread and fillings in the kitchen to make a gluten-free sandwich. The action will use up the bread and the content. ",
    },
    "move_tray" : {
        "detailed": "Moves a tray from one place to another.",
        "layman": "Take the tray from p1 and place it at p2.",
    },
    "put_on_tray" : {
        "detailed": "Places a sandwich from the kitchen onto a tray.",
        "layman": "Place the sandwich on a tray. Now the sandwich is no more at kitchen but on the tray.",
    },
    "serve_sandwich" : {
        "detailed": "Serves a sandwich to a child not allergic to gluten, who is waiting at a specific place. Removes the sandwich from the tray.",
        "layman": "Serve the sandwich from the tray to the child without any specific requests. You need to go to the child place and make sure the child is waiting for the correct sandwich.",
    },
    "serve_sandwich_no_gluten" : {
        "detailed": "Serves a gluten-free sandwich to a child allergic to gluten, who is waiting at a specific place. Removes the sandwich from the tray.",
        "layman": "Serve the gluten-free sandwich from the tray to the child. You need to go to the child place and make sure the child is waiting for the correct sandwich.",
    },
}

PREDICATE_DESC_LST = [
    "(at_kitchen_bread ?b - bread-portion) ;; the bread portion is at the kitchen",
    "(at_kitchen_content ?c - content-portion) ;; the content portion is at the kitchen",
    "(at_kitchen_sandwich ?s - sandwich) ;; the sandwich is at the kitchen",
    "(no_gluten_bread ?b - bread-portion) ;; the bread portion is gluten-free",
    "(no_gluten_content ?c - content-portion) ;; the content portion is gluten-free",
    "(ontray ?s - sandwich ?t - tray) ;; the sandwich is on the tray",
    "(no_gluten_sandwich ?s - sandwich) ;; the sandwich is gluten-free",
    "(allergic_gluten ?c - child) ;; the child is allergic to gluten",
    "(not_allergic_gluten ?c - child) ;; the child is not allergic to gluten",
    "(served ?c - child) ;; the child is served",
    "(waiting ?c - child ?p - place) ;; the child is waiting at the place",
    "(at ?t - tray ?p - place) ;; the tray is at the place",
    "(not_exist ?s - sandwich) ;; the sandwich does not exist",
]