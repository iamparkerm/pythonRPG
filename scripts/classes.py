"""Original game entities and rules; messages are sent to an injected collector."""

import random

#Classes: Character(parent), Enemy(child), Boss(Enemy-child), Player(child).
class Character:
    def __init__(self, rng=None, emit=None):
        self.rng = rng if rng is not None else random.Random()
        self.messages = []
        self.emit = emit if emit is not None else self.messages.append
        self.name = ""
        self.knowledge = 1
        self.knowledge_max = 1
        self.special_charges = 2
        self.specialname = ""

    def do_damage(self, enemy):
        damage = min(max(self.rng.randint(0, self.knowledge) - self.rng.randint(0, enemy.knowledge), 0), enemy.knowledge)
        enemy.knowledge -= damage
        if damage == 0:
            self.emit("{} counters {}'s argument!".format(enemy.name, self.name))
        else:
            self.emit("{}'s argument hurts {}'s feelings!".format(self.name, enemy.name))
            self.emit("{}: knowledge = {}".format(enemy.name, enemy.knowledge))
        return enemy.knowledge <= 0

    def do_maxdamage(self, enemy):
        enemy.knowledge = 0
        return enemy.knowledge <= 0


class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self, player.rng, player.emit)
        if player.knowledge == 1:
            self.knowledge = 1
        else:
            self.knowledge = self.rng.randint(1, player.knowledge - 1)
        self.name = self.rng.choice(enemylist)

    def quote(self):
        self.emit(self.rng.choice(enemy_quote))


class Boss(Enemy):
    def __init__(self, rng=None, emit=None):
        Character.__init__(self, rng, emit)
        self.name = 'Marxist Professor'
        self.knowledge = 20


class Player(Character):
    def __init__(self, rng=None, emit=None):
        Character.__init__(self, rng, emit)
        self.state = 'normal'
        self.knowledge = 7
        self.knowledge_max = 8
        self.enemy = None
        self.playerbooks = [journal]

    @property
    def books(self):
        return len(self.playerbooks)

    def help(self):
        self.emit("Available commands (only first letter is required):")
        for keys in Commands.keys():
            self.emit(keys)

    def stats(self):
        self.emit("{}'s knowledge: {}/{} special: {} book(s): {}".format(
            self.name, self.knowledge, self.knowledge_max, self.special_charges, self.books)
        )

    def dumber(self):
        if self.knowledge > 1:
            self.emit("{} feels a little dumber now.".format(self.name))
            self.knowledge -= 1

    def backpack(self):
        if not self.playerbooks:
            self.emit("{}'s backpack is empty.".format(self.name))
        for book in self.playerbooks:
            self.emit(book[1])

    def read_book(self):
        # Preserve the original author priority, independent of pickup order.
        for book in (Sagan, Vonnegut, Deutsch, Harris, Feynman, journal):
            if book in self.playerbooks:
                if book == journal:
                    self.emit("{} takes out his journal and reads a passage from his journal{}: \n".format(
                        self.name, book[0]))
                else:
                    self.emit("{} takes out a book and reads a passage from {}: \n {}".format(
                        self.name, book[1], book[0]))
                self.playerbooks.remove(book)
                return True
        self.emit("{}'s backpack is empty.".format(self.name))
        return False

    def choose_book(self, choice):
        """Resolve the library choice on a later turn, without terminal input."""
        if choice == '0':
            self.emit("Sorry, you didn't pick a book this visit.")
        elif choice in BOOK_CHOICES:
            self.playerbooks.insert(1, BOOK_CHOICES[choice])
        else:
            self.emit("Please choose a book from 1 to 5, or 0 to leave.")
            return
        self.state = 'normal'

    def read(self):
        if self.state != 'normal':
            self.emit("{} is busy and can't learn now!".format(self.name))
            self.enemy_argue()
        else:
            self.emit("{} looks through his books...".format(self.name))
            if self.knowledge < self.knowledge_max:
                if self.read_book():
                    self.knowledge += 1
                    self.emit("{} feels smarter!\n".format(self.name))
                self.stats()
            else:
                self.emit("{} can't get any smarter right now!".format(self.name))
                self.stats()

    def explore(self):
        if self.state != 'normal':
            self.emit("{} is too busy right now!".format(self.name))
            self.enemy_argue()
            return

        self.emit("{} explores campus.\n".format(self.name))
        if self.rng.randint(0, 1):
            self.enemy = Enemy(self)
            self.emit("{} encounters a {}! The {} shrieks:".format(self.name, self.enemy.name, self.enemy.name))
            self.enemy.quote()
            self.state = 'argue'
        elif self.rng.randint(0, 1):
            self.emit("{} finds a flyer pointing him towards today's big free speach rally and corrects his course.".format(self.name))
        elif self.rng.randint(0, 1):
            self.emit("{} stumbles upon a library! Choose a book from the below shelf to take with you:".format(self.name))
            self.emit("\nCarl Sagan? type 1 \nKurt Vonnegut? press 2 \nDavid Deutsch? press 3 \nSam Harris? press 4 \nRichard Feynman? press 5\nLeave without a book? press 0")
            self.state = 'book_choice'
        elif self.rng.randint(0, 1):
            self.emit("Oops, {} realized he just walked in a circle...".format(self.name))
            self.dumber()
        else:
            self.emit("{} ventures further toward the liberal arts halls.".format(self.name))

    def flee(self):
        if self.state != 'argue':
            self.emit("{} doesn't see anyone to flee from right now.".format(self.name))
            self.dumber()
        else:
            if self.rng.randint(1, self.knowledge + 5) > self.rng.randint(1, self.enemy.knowledge):
                self.emit("{} escaped from the {}.".format(self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
            else:
                self.emit("{} couldn't escape from the {}!".format(self.name, self.enemy.name))
                self.enemy_argue()

    def quit(self):
        self.state = 'quit'

    def _finish_encounter(self, increase_maximum):
        self.enemy = None
        self.state = 'normal'
        self.knowledge += 1
        if increase_maximum:
            self.knowledge_max += 1
        self.emit("{} feels smarter!".format(self.name))

    def argue(self):
        if self.state != 'argue':
            self.emit("{} orates into the air at no one in particular. No one takes the bait.".format(self.name))
        else:
            if self.do_damage(self.enemy):
                self.emit("{} vanquishes the {}!".format(self.name, self.enemy.name))
                self._finish_encounter(increase_maximum=True)
            else:
                self.enemy_argue()

    def special(self):
        if self.special_charges <= 0:
            self.emit("{} is out of special skills!".format(self.name))
            if self.state == 'argue':
                self.enemy_argue()
        elif self.state != 'argue':
            self.emit("{} tests his skill at no one in particular. A lone LARPer in the distance is nonplussed.".format(
                self.name))
            self.dumber()
            self.special_charges -= 1
        else:
            self.emit(
                "{} uses {} ... it's super effective!!! \n {} rekt the {}!".format
                (self.name, self.specialname, self.name, self.enemy.name))
            self.do_maxdamage(self.enemy)
            self.special_charges -= 1
            # Preserve the original special reward: current knowledge only.
            self._finish_encounter(increase_maximum=False)

    def enemy_argue(self):
        if self.enemy.do_damage(self):
            self.emit(
                "({} was rekt by the {}!!!\n {} heads home to join a fantasy football league in shame.\nPlease restart the game.".format(
                    self.name, self.enemy.name, self.name))
###DICTS
enemy_quote = [" 'Biological sex is a social construct!' ", " 'You're oppressing my safe space!' ",
               " '*snap*! *snap*! *snap*! *snap*!' ", " 'You're appropriating the culture of a protected class!' ",
               "'Look! A member of the patriarchy! I'll get him!'", "'I find your privileges more virtuous than mine!'"]
journal = ("\n'Remember to check off your habitica dailies.'\n", "your trusty journal")
Feynman = ("\n'The sole test of the validity of any idea is experiment.'\n",
           "'Freshman Physics Lessons' -by Richard Feynman")
Harris = (
    "\n'If someone doesnt value evidence, what evidence are you going to provide to prove that they should value it?'\n",
    "'Free Will' -by Sam Harris")
Deutsch = (
    "\n'But one thing that all conceptions of the Enlightenment agree on is that it was a rebellion, and specifically a rebellion against authority in regard to knowledge.'\n",
    "'Beginning of Infinity' -by David Deutsch")
Vonnegut = (
    "\n'Beware of the man who works hard to learn something, learns it, and finds himself no wiser than before. He is full of murderous resentment of people who are ignorant without having come by their ignorance the hard way.'\n",
    "'Cat\'s Cradle' -by Kurt Vonnegut")
Sagan = ("\n'Smoke weed every day.'\n", "'Cosmos' -by Carl Sagan")

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
    'P5': ['Parker', 'REKRAP ASTRAL PLANE!']}

BOOK_CHOICES = {'1': Sagan, '2': Vonnegut, '3': Deutsch, '4': Harris, '5': Feynman}
