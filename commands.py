#!/usr/bin/python3

import os
import time
import random
from misadventure import *
from player import *
from normalise import *

def execute_command(command):

    if 0 == len(command):
        return

    if command[0] != "go" and player.current_room == rooms["treasure"]:
        import deaths
        kill_player()
        end()

    if command[0] == "go":
        if len(command) > 1:
            # Correct the player's input if they enter "north east" instead of "northeast"
            # in the corridor, or "south west" instead of "southwest" in the treasure room
            if player.current_room == rooms["corridor"] and len(command) == 3:
                if command[1] == "north" and command[2] == "east":
                    command[1] = "northeast"
            elif player.current_room == rooms["treasure"] and len(command) == 3:
                if command[1] == "south" and command[2] == "west":
                    command[1] = "southwest"
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    elif command[0] == "use":
        if len(command) > 1:
            execute_use(command[1])
        else:
            print("Use what?")
    elif command[0] == "inspect":
        if len(command) > 1:
            execute_inspect(command[1])
        else:
            print("Inspect what?")
    elif command[0] == "exit":
        user_input = str(input("Are you sure you want to give up and exit like a total failure?? YES or NO: ")).lower()
        if user_input == "yes" or user_input == "y":
            print("Just so you know, we are all angry AND dissapointed in you. tsk tsk.")
            options("Q")
        else:
            print("Good answer. Let's keep questing xD")
    elif command[0] == "jump":
        print("Wasn't that fun?")
    elif command[0] == "lick":
        print("...You are pretty weird aren't you. Anyway you've just been poisoned. Well done kid.")
        time.sleep(3)
        end()
    elif command[0] == "cry":
        print("You cannot see through your tears and stumble into your death.")
        time.sleep(3)
        end()
    elif command[0] == "shout":
        print("Good job, now the beast knows you're here. (This means you're definitely dead)")
        time.sleep(3)
        end()
    else:
        print("This makes no sense.")
        player.gibberish += 1

def execute_inspect(item_id):
    item_found = False
    if item_id == "floor":
        print(player.current_room["floor"])
    elif item_id == "ceiling":
        print(player.current_room["ceiling"])
    else:
        for item in player.inventory:
            if item["id"] == item_id:
                print(item["description"])
                item_found = True
                break
        for item in player.current_room["items"]:
            if item["id"] == item_id:
                print(item["description"])
                item_found = True
                break
        if item_found == False:
            print("You try looking for " + item_id + " here, but alas it appears to be absent!.")
    time.sleep(2) # Delay before prompting for next command
def execute_use(item_id):
    #This function is so that the player can use items for various functions
    if not (player.inventory):
        print("You have nothing in your inventory to use, perhaps your memory is failing you?")
    else:
        for item in player.inventory:
            if item['id'] == item_id:
                if item['use_func']():
                    if (item['use']) == "removeable":
                        player.inventory.remove(item)
                    break

        if item_id not in (item["id"]):
            print("You cannot use that.")

def execute_go(direction):

    if direction in player.current_room["exits"]:
        if player.current_room == rooms["dragon room"] and direction == "south":
            if not rooms["boss"]["boss_alive"] and not item_key in player.inventory:
                print("""
                    You missed the key. Oh come on, how the hell do you miss the ONLY thing you had to get? How incompetent can one person be?""") # Make harsher
                time.sleep(1)
            else:
                if item_key in player.inventory:
                    item_key["use_func"]()

                player.attempts += 1

                if player.attempts >= 7:
                    print("Alright fine! I'm done with you and I'm done with my clearly useless existence!")
                    time.sleep(2)
                    exit()
                else:
                    print(player.attempt_exit[player.attempts -1])
                    time.sleep(1)

        # Player asked if they want to enter boss room if they have no items
        elif player.current_room == rooms["corridor"] and direction == "north" and len(player.inventory) == 0 and rooms["boss"]["boss_alive"]:
            choice = str(input("You have no items.\nWould you like to enter the boss room empty handed?\n> ")).lower()
            if choice == "y" or choice == "yes":
                print("""You bravely challenge the beast to a duel. The troll crushes your head in one blow and swings your body around the room, 
                    painting the room in blood. Who knew trolls liked to decorate?""")
                time.sleep(3)
                end()
        elif player.current_room == rooms["boss"] and item_sword in player.inventory and rooms["boss"]["boss_alive"]:
            print("How do expect to run with that sword?")
            time.sleep(1.3)
        else:
            player.current_room = move(player.current_room["exits"], direction)
    else:
        print("You cannot go there. Do you SEE that in the options? Should have gone to specsavers.")

def execute_take(item_id):

    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """
    if not (player.current_room["items"]): #checks if there is a value
        print("There is nothing here to take") #if no value
    else:
        for item in player.current_room["items"]: #itterates over items and compares values
            if item["id"] == item_id:
                if item["name"] == "a bent sword":
                    print("This sword is clearly damaged, why on earth would you want this?")
                    time.sleep(1)
                player.current_room["items"].remove(item) #removes from the room
                player.inventory.append(item) #adds to player inventory
                print("Took " + item["name"] + ".\n")
                time.sleep(0.5)
                break

        if item_id not in (item["id"]): #if item isn't found in list of takable items
            print("You cannot take that.")

def execute_drop(item_id):

    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    if not (player.inventory): # checks for any value in inventory
        print("You have nothing to drop.")
    else:
        for item in player.inventory: #checks against all values in dictionary
            if item["id"] == item_id:
                player.inventory.remove(item)
                player.current_room["items"].append(item)
                print("Dropped " + item_id + ".") #this is a nice bit I kept, good idea!
                boss_battle_drop()
                break

    if item_id not in (item["id"]): #this is a catch for when an item is not in the dictionary but the dictionary still have values
        print("You cannot drop that.")