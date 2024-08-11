INIT_STATE_DESC = "In the library, there are three books: Book1, Book2, and Book3. Book3 is on top of Book1 and they are both on the shelf, while Book2 is on the table. Book1 can also be considered as on the table it is just at the bottom of the shelf. Both Book2 and Book3 are accessible, meaning they can be interacted with. The library worker's hands are free. Book1 belongs to the Fiction category, Book2 belongs to the NonFiction category, and Book3 belongs to the Reference category."



GOAL_STATE_DESC = "The goal is to have Book2 on top of Book3, and also Book1 on top of Book2."

OBJECT_SNIPPET_STR = """(:objects
    Book1 Book2 Book3 - book
    Fiction Non_Fiction Reference - category
)
"""