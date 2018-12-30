from random import randint
import random

#Classes: Character(parent), Enemy(child), Boss(Enemy-child), Player(child).
class Character:
    def __init__(self):
        self.name = ""
        self.knowledge = 1
        self.knowledge_max = 1
        self.special = 2
        self.specialname = ""
        self.books = 0

    def do_damage(self, enemy):
        damage = min(max(randint(0, self.knowledge) - randint(0, enemy.knowledge), 0), enemy.knowledge)
        enemy.knowledge -= damage
        if damage == 0:
            print("{} counters {}'s argument!".format(enemy.name, self.name))
        else:
            print("{}'s argument hurts {}'s feelings!".format(self.name, enemy.name))
            print("{}: knowledge = {}".format(enemy.name, enemy.knowledge))
        return enemy.knowledge <= 0

    def do_maxdamage(self, enemy):
        enemy.knowledge = 0
        return enemy.knowledge <= 0


class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        if player.knowledge == 1:
            self.knowledge = 1
        else:
            self.knowledge = randint(1, player.knowledge - 1)
        self.name = random.choice(enemylist)

    def quote(self):
        print(random.choice(enemy_quote))


class Boss(Enemy):
    def __init__(self):
        Character.__init__(self)
        self.name = 'Marxist Professor'
        self.knowledge = 20


class Player(Character):
    def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.knowledge = 7
        self.knowledge_max = 8
        self.books = 1
        self.playerbooks = [journal, None, None, None, None, None]

    def help(self):
        print("Available commands (only first letter is required):")
        for keys in Commands.keys():
            print(keys)

    def stats(self):
        print("{}'s knowledge: {}/{} special: {} book(s): {}".format(
            self.name, self.knowledge, self.knowledge_max, self.special, self.books)
        )

    def dumber(self):
        if self.knowledge == 1:
            pass
        else:
            print("{} feels a little dumber now.".format(self.name))
            self.knowledge -= 1

    def backpack(self):
        if self.playerbooks[0]:
            print(self.playerbooks[0][1])
        if self.playerbooks[1]:
            print(self.playerbooks[1][1])
        if self.playerbooks[2]:
            print(self.playerbooks[2][1])
        if self.playerbooks[3]:
            print(self.playerbooks[3][1])
        if self.playerbooks[4]:
            print(self.playerbooks[4][1])
        if self.playerbooks[5]:
            print(self.playerbooks[5][1])
        else:
            print("{}'s backpack is empty.".format(self.name))

    def read_book(self):
        if Sagan in self.playerbooks:
            print("{} takes out a book and reads a passage from {}: \n".format(self.name, self.playerbooks[
                self.playerbooks.index(Sagan)][1]), self.playerbooks[self.playerbooks.index(Sagan)][0])
            self.playerbooks.remove(Sagan)
            self.playerbooks.insert(5, None)
            self.books -= 1
        elif Vonnegut in self.playerbooks:
            print("{} takes out a book and reads a passage from {}: \n".format(self.name, self.playerbooks[
                self.playerbooks.index(Vonnegut)][1]), self.playerbooks[self.playerbooks.index(Vonnegut)][0])
            self.playerbooks.remove(Vonnegut)
            self.playerbooks.insert(4, None)
            self.books -= 1
        elif Deutsch in self.playerbooks:
            print("{} takes out a book and reads a passage from {}: \n".format(self.name, self.playerbooks[
                self.playerbooks.index(Deutsch)][1]), self.playerbooks[self.playerbooks.index(Deutsch)][0])
            self.playerbooks.remove(Deutsch)
            self.playerbooks.insert(3, None)
            self.books -= 1
        elif Harris in self.playerbooks:
            print("{} takes out a book and reads a passage from {}: \n".format(self.name, self.playerbooks[
                self.playerbooks.index(Harris)][1]), self.playerbooks[self.playerbooks.index(Harris)][0])
            self.playerbooks.remove(Harris)
            self.playerbooks.insert(2, None)
            self.books -= 1
        elif Feynman in self.playerbooks:
            print("{} takes out a book and reads a passage from {}: \n".format(self.name, self.playerbooks[
                self.playerbooks.index(Feynman)][1]), self.playerbooks[self.playerbooks.index(Feynman)][0])
            self.playerbooks.remove(Feynman)
            self.playerbooks.insert(1, None)
            self.books -= 1
        else:
            print("{} takes out his journal and reads a passage from his journal{}: \n".format(self.name,
                                                                                               self.playerbooks[0][0]))
            self.playerbooks.remove(journal)
            self.playerbooks.insert(0, None)
            self.books -= 1

    def read(self):
        if self.state != 'normal':
            print("{} is busy and can't learn now!".format(self.name))
            self.enemy_argue()
        else:
            print("{} looks through his books...".format(self.name))
            if self.knowledge < self.knowledge_max:
                self.read_book()
                self.knowledge += 1
                print("{} feels smarter!\n".format(self.name))
                self.stats()
            else:
                print("{} can't get any smarter right now!".format(self.name))
                self.stats()

    def explore(self):
        if self.state != 'normal':
            print("{} is too busy right now!".format(self.name))
            self.enemy_argue()
        else:
            print("{} explores campus.\n".format(self.name))
            if randint(0, 1):
                self.enemy = Enemy(self)
                print("{} encounters a {}! The {} shrieks:".format(self.name, self.enemy.name, self.enemy.name))
                self.enemy.quote()
                self.state = 'argue'
            else:
                if randint(0, 1):
                    print(
                        "{} finds a flyer pointing him towards today's big free speach rally and corrects his course.".format(
                            self.name))
                else:
                    if randint(0, 1):
                        print("{} stumbles upon a library! Choose a book from the below shelf to take with you:".format(
                            self.name))
                        new_book = eval(input(
                            "\nCarl Sagan? type 1 \nKurt Vonnegut? press 2 \nDavid Deutsch? press 3 \nSam Harris? press 4 \nRichard Feynman? press 5"))
                        if new_book == 1:
                            new_book = Sagan
                            self.playerbooks.insert(1, new_book)
                            self.books += 1
                        elif new_book == 2:
                            b = Vonnegut
                            self.playerbooks.insert(1, b)
                            self.books += 1
                        elif new_book == 3:
                            b = Deutsch
                            self.playerbooks.insert(1, b)
                            self.books += 1
                        elif new_book == 4:
                            b = Harris
                            self.playerbooks.insert(1, b)
                            self.books += 1
                        elif new_book == 5:
                            b = Feynman
                            self.playerbooks.insert(1, b)
                            self.books += 1
                        else:
                            print("Sorry, you didn't pick a book this visit.")
                    else:
                        if randint(0, 1):
                            print("Oops, {} realized he just walked in a circle...".format(self.name))
                            self.dumber()
                        else:
                            print("{} ventures further toward the liberal arts halls.".format(self.name))

    def flee(self):
        if self.state != 'argue':
            print("{} doesn't see anyone to flee from right now.".format(self.name))
            self.dumber()
        else:
            if randint(1, self.knowledge + 5) > randint(1, self.enemy.knowledge):
                print("{} escaped from the {}.".format(self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
            else:
                print("{} couldn't escape from the {}!".format(self.name, self.enemy.name))
                self.enemy_argue()

    def quit(self):
        exit()

    def argue(self):
        if self.state != 'argue':
            print("{} orates into the air at no one in particular. No one takes the bait.".format(self.name))
        else:
            if self.do_damage(self.enemy):
                print("{} vanquishes the {}!".format(self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
                self.knowledge += 1
                self.knowledge_max += 1
                print("{} feels smarter!".format(self.name))
            else:
                self.enemy_argue()

    def special(self):
        if self.state != 'argue':
            print("{} tests his skill at no one in particular. A lone LARPer in the distance is nonplussed.".format(
                self.name))
            self.dumber()
            self.special -= 1
        else:
            if self.special > 0:
                print(
                    "{} uses {} ... it's super effective!!! \n {} rekt the {}!".format
                    (self.name, self.specialname, self.name, self.enemy.name))
                self.do_maxdamage
                self.enemy = None
                self.state = 'normal'
                self.knowledge += 1
                self.special -= 1
                print("{} feels smarter!".format(self.name))
            else:
                print("{} is out of special skills!".format(self.name))
                self.enemy_argue()

    def enemy_argue(self):
        if self.enemy.do_damage(self):
            print(
                "({} was rekt by the {}!!!\n {} heads home to join a fantasy football league in shame.\nPlease restart the game.".format(
                    self.name, self.enemy.name, self.name))
###DICTS
enemy_quote = [" 'Biological sex is a social construct!' ", " 'You're oppressing my safe space!' ",
               " '*snap*! *snap*! *snap*! *snap*!' ", " 'You're appropriating the culture of a protected class!' ",
               "'Look! A member of the patriarchy! I'll get him!'", "'I find your privileges more virtuous than mine!'"]
journal = ["\n'Remember to check off your habitica dailies.'\n", "your trusty journal"]
Feynman = ["\n'The sole test of the validity of any idea is experiment.'\n",
           "'Freshman Physics Lessons' -by Richard Feynman"]
Harris = [
    "\n'If someone doesnt value evidence, what evidence are you going to provide to prove that they should value it?'\n",
    "'Free Will' -by Sam Harris"]
Deutsch = [
    "\n'But one thing that all conceptions of the Enlightenment agree on is that it was a rebellion, and specifically a rebellion against authority in regard to knowledge.'\n",
    "'Beginning of Infinity' -by David Deutsch"]
Vonnegut = [
    "\n'Beware of the man who works hard to learn something, learns it, and finds himself no wiser than before. He is full of murderous resentment of people who are ignorant without having come by their ignorance the hard way.'\n",
    "'Cat\'s Cradle' -by Kurt Vonnegut"]
Sagan = ["\n'Smoke weed every day.'\n", "'Cosmos' -by Carl Sagan"]

enemylist = ['Social Justice Warrior', 'Libtard', 'White Knight']

# Dictionaries ('key':'value' pairs)
Commands = {
    'help': Player.help, 'stats': Player.stats,
    'backpack': Player.backpack, 'explore': Player.explore,
    'argue': Player.argue, 'read': Player.read, 'use special': Player.special,
    'flee': Player.flee, 'quit': Player.quit}

PlayerDict = {
    'P1': ['Corey', 'VERY ACCURATE THROW!'],
    'P2': ['Eric', 'PARTYING DAD!'],
    'P3': ['Josh', 'RETARD STRENGTH!'],
    'P4': ['Kevin', 'AVOIDS CONFRONTATION!'],
    'P5': ['Parker', 'BELLIGERENT SMARM!']}
