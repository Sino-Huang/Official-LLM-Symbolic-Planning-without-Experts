INIT_STATE_DESC = """In the dungeon, the hero starts at cell5, with free hands ready for action. The hero is aware of the dungeon's layout, which consists of multiple interconnected cells. A sword is located in cell4. The dungeon contains dangerous monsters located in cell3 and cell8, and a trap is present in cell2. The hero must navigate this treacherous environment, using the connections between the cells to move around. The connections are as follows:

    Cell1 is connected to cell2.
    Cell2 is connected to cell1 and cell3.
    Cell3 is connected to cell2 and cell4.
    Cell4 is connected to cell3 and cell5.
    Cell5 is connected to cell4 and cell8.
    Cell6 is connected to cell7.
    Cell7 is connected to cell6 and cell8.
    Cell8 is connected to cell7 and cell5.
    Cell2 is also connected to cell6.
    Cell3 is also connected to cell7.
    Cell4 is also connected to cell8.
"""



GOAL_STATE_DESC = "The hero's ultimate objective is to reach cell1 safely."

OBJECT_SNIPPET_STR = """(:objects
    cell1 cell2 cell3 cell4 cell5 cell6 cell7 cell8 - cells
    sword1 - swords
)
"""