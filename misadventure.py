#!/usr/bin/python3

import os
import time
import random
from normalise import *
from player import *
from commands import *


if __name__ == "__main__":
	import os
	main()

def main():
    try:
        rooms["armoury"]["ceiling"] = rooms["armoury"]["ceiling"].format(player.name)
        # Main game loop
        while True:
            
            # Display game status (room description, inventory etc.)
            fail_conditions(player.current_room)
            print_room(player.current_room)
            print_inventory_items(player.inventory)

            # Show the menu with possible actions and ask the player
            command = menu(player.current_room["exits"], player.current_room["items"], player.inventory)

            # Execute the player's command
            execute_command(command)
    except KeyboardInterrupt:
        # When exception is keyboard interrupt, quit gracefully
        print("I'd have thought you'd put more effort in than that...")
        print("Exited game.")
        exit()
    except SystemExit:
        exit()
    except:
        names = ["James", "Luca", "Alastair", "Dervla", "Natalie", "Sam"]
        print("Ah, an error. " + names[random.randrange(0, len(names))] + " didn't code that bit properly.")
        exit()

def menu(exits, room_items, inv_items):


    # Display menu
    print_menu(exits, room_items, inv_items)
    
    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input

