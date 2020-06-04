from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", Item("stick", """I could use this to poke around...""")),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", Item("flashlight", """Maybe this could help me see...""")),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", Item("gold", """You find some gold!""")),
}

# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player("Alex", room['outside'])

# print(player)

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

# actions available to user
moves = ['n', 's', 'e', 'w']
actions = ['i', 'inventory']

# welcome the user and give them instructions on how to play
print("Welcome, adventurer. Explore until you find the treasure!")
print("*" * 70)
print("CONTROLS:")
print(
    "Move using [n] north, [s] south, [e] east, and [w] west.")
print(
    "Pickup items using [get ItemName], drop items using [drop ItemName], or quit [q]")
print("*" * 70)

while True:
    print("Current Area: " + player.current_room.name)
    print(player.current_room.description)

    # if there are any available items in the room, display them to the player
    for item in player.current_room.items:
        print(f"You see a(n) {item}")

    print('What would you like to do?\n')
    player_input = input("> ")

    if player_input == 'q':  # quit the game if the user inputs q
        exit()
    elif player_input in moves:  # if the user selects a direction to move, use our move method
        player.move(f'{player_input}_to')
    elif player_input in actions:  # if the user opens their inventory, use our display inventory method
        player.display_inventory()
    elif "get" in player_input or "take" in player_input:
        # if user inputs "get" or "take", determine if they've entered in
        # a valid item that exists in the room, and use our pickup method
        print("Attempting to pick up item...")
        words = player_input.split()

        if len(words) > 1:
            selection = words[1]
            found_item = player.current_room.does_item_exist(selection)

            print(found_item)
            if found_item:
                player.pickup_item(found_item)
                player.current_room.remove_item(found_item)
        else:
            print("What are you trying to pickup?") # the user did not input an item, or it didn't exist

    elif "drop" in player_input:
        # if the user inputs "drop", determine if they've entered in a
        # valid item that exists in their inventory, and use our drop method
        print("Attempting to drop...")
        words = player_input.split()

        if len(words) > 1:
            selection = words[1]
            found_item = player.find_item(selection)

            if found_item:
                player.current_room.add_item(found_item)
                player.drop_item(found_item)
        else:
            print("What do you want to drop?") # the user did not input an item, or it didn't exist
