"""
Name: 
Last updated: 
Description: 
"""

def adventure():
    """ This function runs one session of a choose your own adventure.
        Arguments: None
        Returns: None (Printed text is not returned)
    """

    print()

    print("Welcome, worthy adventurer, to The Swamp,")
    print("home to Ally the Golden Gator and sourdough bread!")

    print()

    player_name, player_class = create_player()

    print()
    
    if player_class == "Warrior":
        health = 100
        mana = 50
        print("A brave warrior, ready to confront any challenge.")

    elif player_class == "Mage":
        health = 50
        mana = 100
        print("A cunning mage, capable of outwitting the strongest foe.")

    print()

    print("Here are your beginning stats:")
    print("Health: {}".format(health))
    print("Mana: {}".format(mana))

    print()

    print(player_name, "your quest is to rescue Ally from the Spartans")
    print("who hold her captive.")
    print("Let us begin...")

    # Add branches to the adventure here!

    path = input("You see one cave entrance and one cave exit. Which do you choose? [Enter 'entrance' or 'exit'] ")

    if path == "entrance":
        print("You have entered the cave and find a Dragon! You have been scorched but barely alive. You have lost 40 health points.")

        health = health - 40
        print("Health: {}".format(health))

        path2 = input("Do you run out the cave exit or do you fight the Dragon? [Enter 'exit' or 'fight'] ")

        if path2 == "fight":
            print("You have died, in your hubris you lost sight of the goal and died in the cave. You have lost the game.")
            return 1

        elif path2 == "exit":
            print("You escape and set off on the path of killers and dreamers.")
            print("You leave the cave and find Ally...above a pile of dead Spartans...so much for the rescue mission. You have won the game!")
            return 1

    elif path == "exit":
        print("You escape and set off on the path of killers and dreamers.")
        print("You leave the cave and find Ally...above a pile of dead Spartans...so much for the rescue mission. You have won the game!")
        return 1


def create_player():
    """ Prompts the user for their name and class.
        Arguments: None
        Returns:
            - player_name (string): Name of the player
            - player_class (string): Class of the player
    """

    player_name = input("Before we begin, what should I call you? ")
    player_class = input("What is your specialty? [Warrior / Mage] ")

    while player_class != "Warrior" and player_class != "Mage":
        print("I do not recognize that specialty. Please choose either Warrior or Mage.")
        player_class = input("What is your specialty? [Warrior / Mage] ")

    return player_name, player_class


win = 0
while win == 0:
    win = adventure()