DOMAIN_DESC = "This domain is structured to allow organizing and managing books within a library setting. The actions and predicates support the movement of books between tables and shelves, ensuring that conditions like accessibility and the librarian's hands being free are met. Additionally, it includes managing book categories, shelf space, and check-out/return processes to reflect a more complex library system."

ACTION_DESC_DICT = {
    "take-from-table": {
        "detailed": "Imagine you're a librarian managing a table full of books. The 'take-from-table' action allows you to pick up a book that is on the table, provided it is accessible and your hands are free. This action simulates the scenario where you find a book on the table, ensure it's not covered by any other book, and then pick it up, thus holding it in your hands.",
        "layman": "Pick up a book from the table if it's not covered and your hands are empty.",
    },
    "place-on-table": {
        "detailed": "Picture a librarian holding a book. The 'place-on-table' action involves placing the held book onto the table. This action is feasible if the librarian is currently holding the book. Once placed, the book becomes accessible again, and the librarian's hands are free.",
        "layman": "Put a book you're holding onto the table, making it accessible.",
    },
    "place-on-shelf": {
        "detailed": "Consider a librarian holding a book and standing near a shelf. The 'place-on-shelf' action involves placing the held book on top of another book on the shelf, given that the book on the shelf is accessible. This action results in the held book becoming accessible, the book on the shelf becoming inaccessible, and the librarian's hands becoming free.",
        "layman": "Put a book you're holding on top of another accessible book on the shelf.",
    },
    "remove-from-shelf": {
        "detailed": "Imagine a librarian approaching a shelf where one book is placed on top of another. The 'remove-from-shelf' action allows the librarian to take the top book off the shelf, provided it is accessible and the librarian's hands are free. This action makes the book on the shelf accessible and the librarian holds the removed book.",
        "layman": "Pick up an accessible book from the shelf if your hands are empty, making the book underneath accessible.",
    },
    "check-out": {
        "detailed": "Envision a librarian assisting a patron who wishes to borrow a book. The 'check-out' action allows the librarian to mark a book as checked out, provided it is accessible and not already checked out. This action reflects the process of recording the book's status as borrowed and setting a return due date.",
        "layman": "Mark a book as borrowed by a patron, ensuring it's not already taken.",
    },
    "return-book": {
        "detailed": "Imagine a patron returning a borrowed book to the library. The 'return-book' action enables the librarian to process the return, updating the book's status and removing any return due date. This action is applicable when the librarian is holding the book that needs to be returned.",
        "layman": "Record a book as returned by a patron when you're holding it.",
    },
}

PREDICATE_DESC_LST = [
    "(on-shelf ?x ?y - book) ;; ?x is on top of ?y on the shelf",
    "(on-table ?x - book) ;; ?x is on the table",
    "(accessible ?x - book) ;; ?x is accessible (not covered)",
    "(hands-free) ;; The hands of the librarian are free",
    "(holding ?x - book) ;; The librarian is holding ?x",
    "(belongs-to-category ?x - book ?cat - category) ;; ?x belongs to the category ?cat",
    "(shelf-empty ?cat - category) ;; The shelf for category ?cat is empty",
    "(shelf-overflow ?cat - category) ;; The shelf for category ?cat is full",
    "(book-request ?book - book) ;; There is a request for book ?book",
    "(return-due ?book - book) ;; Book ?book is due for return",
    "(checked-out ?book - book) ;; Book ?book is checked out",
]

TYPE_INFO_STR = "(:types book category)"
