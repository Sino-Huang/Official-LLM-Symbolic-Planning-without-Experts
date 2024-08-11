DOMAIN_DESC = "This domain definition sets up a basic framework for actions and interactions in a simplified Minecraft-like environment, focusing on movement, item management, and basic crafting."

ACTION_DESC_DICT = {
    "craft_plank" : {
        "detailed": "In the world of Minecraft, crafting is a key skill, and here, the agent can turn a log into planks. It's a bit like a magic trick: the agent takes a log, which they have to be holding, and transforms it into planks. These planks then appear in their inventory, ready to be used for building or crafting other items. The log, of course, is used up in this process.",
        "layman":"craft var0 into a plank using var2 log.",
    },
    "equip" : {
        "detailed": "This is when the agent decides to take something out of their inventory and hold it in their hands, ready for use. It could be picking up a tool for chopping or a weapon for defense. Once they equip an item, their hands are no longer empty - they're now holding this item, ready to use it for whatever task they have in mind.",
        "layman":"equip var0 from inventory and thus agent var1 has something in his hand ",
    },
    "move" : {
        "detailed": "This is the agent's way of getting from one spot to another. Think of it as walking, running, or hopping across the Minecraft world. When the agent decides to move, they leave their current spot and end up at a new location. It's a simple action but essential for exploring the world and getting to different resources or areas.",
        "layman":"move from var1 to var0",
    },
    "pick" : {
        "detailed": "Picture the agent spotting something valuable or useful on the ground, like a piece of fruit or a tool. The pick action is them bending down and picking up this item, adding it to their inventory. It's a fundamental action for gathering resources as they explore the Minecraft environment. Once picked, the item is no longer lying around; it's safely stored in the agent's inventory.",
        "layman":"pick var0 at var1 location",
    },
    "recall" : {
        "detailed": "Imagine the agent (like a Minecraft player) has an ability to teleport an item they are currently using (equipped) straight into their inventory. That's what the recall action does. It's like saying, 'Okay, I'm done with this axe; let's magically put it back in my backpack.' This action not only puts the item away but also ensures that the agent's hands are now empty and ready for something else.",
        "layman":"put a moveable back to inventory",
    },
}

PREDICATE_DESC_LST = [
    "(is_grass ?arg0 - moveable) ;; the object is grass",
    "(is_log ?arg0 - moveable) ;; the object is a log",
    "(is_planks ?arg0 - moveable) ;; the object is a plank",
    "(at ?arg0 - moveable ?arg1 - static) ;; the object is at a location",
    "(agent_at ?arg0 - static) ;; the agent is at a location",
    "(inventory ?arg0 - moveable) ;; the object is in the agent's inventory",
    "(hypothetical ?arg0 - moveable) ;; the object is hypothetical",
    "(equipped ?arg0 - moveable ?arg1 - agent) ;; the agent is holding the object",
    "(handsfree ?arg0 - agent) ;; the agent has empty hands",
]

TYPE_INFO_STR = """(:types
    moveable static agent
)"""