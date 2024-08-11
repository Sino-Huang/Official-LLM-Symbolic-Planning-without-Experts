DOMAIN_DESC = "In this logistics domain, various objects need to be transported from one location to another. To achieve this, trucks are used for moving objects within a city, while airplanes are used for transporting objects between different cities. The domain includes different types of locations such as regular places and airports, with specific vehicles designed for each type of transport."

ACTION_DESC_DICT = {
    'load-truck' : {
        "detailed": "When you need to transport an object within a city, you can load it onto a truck. This involves placing the object inside the truck at a specific location. The object and the truck must both be at the same location for this action to take place. Once loaded, the object is ready to be moved by the truck.",
        "layman": "This action enables the agent to load a package into a truck. For example, load a package_1 into a truck_1.",
    },
    'load-airplane' : {
        "detailed": "For long-distance transportation, objects are loaded onto airplanes. This requires that the object and the airplane are at the same location, typically an airport. Once the object is loaded into the airplane, it can be flown to another city. This action removes the object from its current location and places it inside the airplane.",
        "layman": "This action enables the agent to load a package into an airplane. For example, load a package_1 into an airplane_1.",
    },
    'unload-truck' : {
        "detailed": "After a truck has transported an object to its destination within the city, the object needs to be unloaded. This action takes the object out of the truck and places it at the new location. The truck and the object must both be at the same location for the unloading to occur.",
        "layman": "This action enables the agent to unload a package from a truck. For example, unload a package_1 from a truck_1.",
    },
    'unload-airplane' : {
        "detailed": "Similar to unloading a truck, this action involves removing an object from an airplane once it has reached its destination. The object is taken out of the airplane and placed at the airport or specified location. The airplane must be at the same location as the object for this action to happen.",
        "layman": "This action enables the agent to unload a package from an airplane. For example, unload a package_1 from an airplane_1.",
    },
    'drive-truck' : {
        "detailed": "Trucks can drive from one location to another within the same city. To move a truck, you specify the starting location, the destination location, and the city. The truck travels from the starting point to the endpoint, making it available for loading or unloading objects at the new location.",
        "layman": "This action enables the agent to drive a truck from one location to another in a city. For example, drive a truck_1 from location_1 to location_2 in city_1.",
    },
    'fly-airplane' : {
        "detailed": "Airplanes are used to fly objects between different cities. This action involves moving the airplane from one airport to another. The airplane must start at the departure airport and will end up at the destination airport, ready for unloading or further transportation of the objects inside.",
        "layman": "This action enables the agent to fly an airplane from one city's airport to another. The airports are locations in the city. For example, fly an airplane_1 from location_0 to location_1.",
    },
}

PREDICATE_DESC_LST = [
    '(at ?obj - object ?loc - location) ;; the object is at the location',
    '(in ?obj1 - object ?obj2 - object) ;; the obj1 is in obj2',
    '(in-city ?loc - location ?city - city) ;; the location is in the city',
]