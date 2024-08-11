DOMAIN_DESC = "Moving and storing crates of goods by hoists from containers to depots with spatial maps. This domain deals with the movement and storage of crates of goods using hoists. It involves different locations like containers and depots, and requires managing the spatial arrangement of crates and hoists in various areas. The actions primarily focus on the lifting, moving, and placement of crates by hoists, considering the spatial and availability constraints of the areas involved."



ACTION_DESC_DICT = {
    "drop" : {
        "detailed" : "This action is about a hoist dropping a crate into a store_area from an area. Preconditions are similar to 'Lift' but include the hoist lifting the crate and the destination store_area being clear. The effects involve the hoist becoming available and the crate being placed on the destination store_area.",
        "layman" : "After moving the crate to a2, drop it",
    },
    "go-in" : {
        "detailed" : "This is the reverse of Go-out, where a hoist moves from a transit_area to a store_area. Preconditions include the hoist being at the transit_area, the areas being connected, and the destination store_area being clear. The effect is similar to Go-out but in reverse.",
        "layman" : "move hoist from transit area back to store area",
    },
    "go-out" : {
        "detailed" : "Involves a hoist moving from a store_area to a transit_area. Preconditions are the hoist being at the source store_area and the areas being connected. The effect is the hoist moving to the transit_area and the source store_area becoming clear.",
        "layman" : "move hoist to transit area. So the previous place will not be occupied",
    },
    "lift" : {
        "detailed" : "Involves a hoist lifting a crate from one store_area to another area. Preconditions include the areas being connected, the hoist being at the destination area and available, and the crate being on the source store_area. The effects are the crate being lifted and the source store_area becoming clear.",
        "layman" : "a1 and a2 warehouses are connected, use the hoist to move the crate from a2 to a1.",
    },
    "move" : {
        "detailed" : "Moves a hoist from one store_area to another. Preconditions include the hoist being at the source store_area, the destination store_area being clear, and the areas being connected. The effect is the hoist moving to the destination and the change in clarity status of both store areas.",
        "layman" : "move hoist from one location to another location, ensure two locations are connected. The movement will occupy the target place.",
    },
}

PREDICATE_DESC_LST = [
    "(clear ?s - store_area) ;; the store area is clear",
    "(crate_in ?c - crate ?p - place) ;; the crate is in the place",
    "(store_area_in ?s - store_area ?p - place) ;; the store area is in the place",
    "(available ?h - hoist) ;; the hoist is available",
    "(lifting ?h - hoist ?c - crate) ;; the hoist is lifting the crate",
    "(at ?h - hoist ?a - area) ;; the hoist is at the area",
    "(on ?c - crate ?s - store_area) ;; the crate is on the store area",
    "(connected ?a1 ?a2 - area) ;; the area a1 is connected to the area a2",
]