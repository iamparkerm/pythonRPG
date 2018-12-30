# updated for python3
import sys
import time
from scripts.classes import *

p = Player()
#Main() is the first function the game runs
def main():
    intro()
    # Loop that begins game
    while p.knowledge < 16:
        line = input("What would you like to do? > ")
        args = line.split()
        if len(args) > 0:
            commandFound = False
            # was Commands.keys: in py2
            for c in Commands:
                # if the first letter[0] in the input is equal to the first letter in the Commands dict value
                if args[0] == c[:len(args[0])]:
                    # then Player.help(Player())
                    Commands[c](p)
                    commandFound = True
                    break
            if not commandFound:
                print("{} doesn't understand the suggestion.".format(p.name))
        if p.knowledge == 0:
            killed_screen()
            break

    # boss battle info
    boss = Boss()
    p.state = 'argue'
    p.enemy = boss
    print(
        "-----------FINAL STAGE------------\n {} joins the free speech rally. "
        "But what is this?! An angry mob wants to de-platform the rally! {} wonders what they're afraid of hearing?"
        " \nBOSS ENCOUNTERED \n {} encounters the {}!".format(p.name, p.name, p.name, boss.name))
    print(
        "\n 'You think we care about OBJECTIVE TRUTH and KNOWLEDGE?!"
        " We only believe in the subjective truths our LIVED EXPERIENCES!"
        " What can you possibly say to deny this??', says the {}".format(boss.name))

    # loop that begins boss battle
    while boss.knowledge > 0:
        line = input("What would you like to do? > ")
        args = line.split()
        if len(args) > 0:
            commandFound = False
            for c in Commands:
                if args[0] == c[:len(args[0])]:
                    Commands[c](p)
                    commandFound = True
                    break
            if not commandFound:
                print("{} doesn't understand the suggestion.".format(p.name))
        if p.state != 'argue':
            kill_screen()
            break


def intro():
    print(
        "Oh, hello, I didn't see you there. You look smart as shit. I bet you're from Owl Town and"
        "\nback on campus for some learning. Well watch out for the big rally today planned over in Red Square.")
    time.sleep(2)
    print("..........."
        "\nSo which one are you, anyway?"
        "\nCorey? type 1 \nEric? press 2 \nJosh? press 3 \nKevin? press 4 \nParker? press 5")
    choice = ''
    while not (choice == 1 or choice == 2 or choice == 3 or choice == 4 or choice == 5):
        try:
            choice = eval(input("Choice ="))
        except NameError:
            print("\nNot an integer! Try again.")
            continue
    if choice == 1:
         p.name = 'Corey'
         p.specialname = 'VERY ACCURATE THROW!'
    elif choice == 2:
         p.name = 'Eric'
         p.specialname = 'PARTYING DAD!'
    elif choice == 3:
         p.name = 'Josh'
         p.specialname = 'RETARD STRENGTH!'
    elif choice == 4:
         p.name = 'Kevin'
         p.specialname = 'AVOIDS CONFRONTATION!'
    elif choice == 5:
         p.name = 'Parker'
         p.specialname = 'REKRAP ASTRAL PLANE!'
    print("\nWelcome, {}. (type help to see what your options are)".format(p.name))

#win game function
def kill_screen():
    print(
        "\n {} vanquished all the post-modernist illiberals! {} has returned freedom of speech to campus! \n".format(
            p.name, p.name))
    print(
        "Hi, this is ReKrap, and thanks for playing. I know we had a lot of fun today, but its important to remember that knowledge is half the battle thumbs up emoji")
    print("developer - ReKrap")
    print("writer - ReKrap")
    print("THE END")
    print("P.S. There's a potential Donkey Kong kill screen coming up if anyone is interested.")

#lose game function
def killed_screen():
    print(
        "Your head feels a little foggy, but you can't think of any response. Maybe you will go home and nap. \nPlease reload the program to play again.")
    sys.exit()

if __name__ == '__main__':
    main()
