from random import randint
import random
import pdb
import ipywidgets as widgets

class Character:
    def __init__(self):
        self.name = ""
        self.knowledge = 1
        self.knowledge_max = 1
        self.special = 2
        self.special_max = 2
        self.specialname = ""
        self.books = 0
    def do_damage(self, enemy):
        damage = min(max(randint(0, self.knowledge) - randint(0, enemy.knowledge), 0), enemy.knowledge)
        enemy.knowledge -= damage
        if damage == 0:
            print "%s counters %s's argument!" % (enemy.name, self.name)
        else: 
            print "%s's logic hurts the %s's feelings!" % (self.name, enemy.name)
            print "%s: knowledge = %d" % (enemy.name, enemy.knowledge)
        return enemy.knowledge <= 0
        print "enemy's knowledge just returned <=0"
    def do_maxdamage(self, enemy):
        enemy.knowledge=0
        return enemy.knowledge <= 0

class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        self.knowledge = randint(1, player.knowledge - 1)
        self.name = random.choice(enemylist)
        
class Player(Character):
    def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.knowledge = 7
        self.knowledge_max = 8
        self.books = 1
        self.playerbooks = [journal, None, None, None, None, None]
    def help(self): print Commands.keys()
#    def quit(self):
#        print "Thanks for playing."
    def stats(self): print "%s's knowledge: %d/%d special: %d/%d book(s): %d" % (self.name, self.knowledge, self.knowledge_max, self.special, self.special_max, self.books)
    def dumber(self):
        print "%s feels a little dumber now." % self.name
        self.knowledge = max(1, self.knowledge - 1)
    def read_book(self):
        if Sagan in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Sagan)[1]]), self.playerbooks[self.playerbooks.index(Sagan)][0]
            self.playerbooks.remove(Sagan)
            self.playerbooks.insert(5, None)
            self.books -=1
        elif Vonnegut in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Vonnegut)[1]]), self.playerbooks[self.playerbooks.index(Vonnegut)][0]
            self.playerbooks.remove(Vonnegut)
            self.playerbooks.insert(4, None)
            self.books -=1
        elif Deutsch in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Deutsch)[1]]), self.playerbooks[self.playerbooks.index(Deutsch)][0]
            self.playerbooks.remove(Deutsch)
            self.playerbooks.insert(3, None)
            self.books -=1
        elif Harris in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Harris)[1]]), self.playerbooks[self.playerbooks.index(Harris)][0]
            self.playerbooks.remove(Harris)
            self.playerbooks.insert(2, None)
            self.books -=1
        elif Feynman in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Feynman)[1]]), self.playerbooks[self.playerbooks.index(Feynman)][0]
            self.playerbooks.remove(Feynman)
            self.playerbooks.insert(1, None)
            self.books -=1
        else:
            print "%s takes out his journal and reads a passage: \n" % self.name, self.playerbooks[0][0]
            self.playerbooks.remove(journal)
            self.playerbooks.insert(0,None)
            self.books -=1
    def read(self):
        if self.state != 'normal':
            print "%s is busy and can't learn now!" % self.name
            self.enemy_argue()
        else: 
            print "%s looks through his books..." % self.name
            if self.playerbooks[0]==None:
                print "%s hasn't found anything else to read yet!" % self.name
                self.stats()
            else:
                if self.knowledge < self.knowledge_max:
                    self.read_book()
                    self.knowledge += 1
                    print "%s feels smarter!\n" % self.name
                    self.stats()                    
                else:
                    print "%s can't get any smarter right now!" % self.name
                    self.stats()
    def explore(self):
        if self.state != 'normal':
            print "%s is too busy right now!" % self.name
            self.enemy_argue()
        else:
            print "%s explores campus.\n" % self.name
            if randint(0, 1):
                self.enemy = Enemy(self)
                print "%s encounters a %s!" % (self.name, self.enemy.name)
                self.state = 'argue'
            else:
                if randint(0, 1):
                    print "%s realized he just walked in a circle..." % self.name
                    self.dumber() 
                else:
                    print "%s stumbles upon a library! Choose a book from the below shelf to take with you:" % self.name
                    new_book = input("\nCarl Sagan? type 1 \nKurt Vonnegut? press 2 \nDavid Deutsch? press 3 \nSam Harris? press 4 \nRichard Feynman? press 5")                   
#                    choice=''
#                    while not (choice==1 or choice==2 or choice==3 or choice==4 or choice==5):
#                        try:
#                            new_book = input("\nCarl Sagan? type 1 \nKurt Vonnegut? press 2 \nDavid Deutsch? press 3 \nSam Harris? press 4 \nRichard Feynman? press 5")
#                        except NameError:
#                            print("\nNot an option! Try again.")
#                            continue
#                        break
                    if new_book==1:
                        new_book=Sagan
                        self.playerbooks.insert(1,new_book)
                        self.books +=1
                    elif new_book==2:
                        b=Vonnegut
                        self.playerbooks.insert(1,b)
                        self.books +=1
                    elif new_book==3:
                        b=Deutsch
                        self.playerbooks.insert(1,b)
                        self.books +=1
                    elif new_book==4:
                        b=Harris
                        self.playerbooks.insert(1,b)
                        self.books +=1
                    elif new_book==5:
                        b=Feynman
                        self.playerbooks.insert(1,b)
                        self.books +=1
                    else:
                        print "Sorry, you didn't pick a book this visit."
                    print "\nNow continue or type 'help' for more options..."
    def flee(self):
        if self.state != 'argue':
            print "%s doesn't see anyone to flee from right now." % self.name
            self.dumber()
        else:
            if randint(1, self.knowledge + 5) > randint(1, self.enemy.knowledge):
                print "%s escaped from the %s." % (self.name, self.enemy.name)
                self.enemy = None
                self.state = 'normal'
            else:
                print "%s couldn't escape from the %s! (╯'□')╯︵ ┻━┻" % (self.name, self.enemy.name)
                self.enemy_argue()
    def argue(self):
        if self.state != 'argue': 
            print "%s orates into the air at no one in particular. No one takes the bait." % self.name
            self.dumber()
            self.stats()
        else:
            if self.do_damage(self.enemy):
                print "%s vanquishes the %s! (╯°Д°）╯︵ /(.□.\) " % (self.name, self.enemy.name)
                self.enemy = None
                self.state = 'normal'
                self.knowledge += 1
                self.knowledge_max += 1
                print "%s feels smarter!" % self.name              
            else: self.enemy_argue() 
    def special(self):
        if self.state != 'argue': 
            print "%s tests his skill at no one in particular. A lone LARPer in the distance is nonplussed." % self.name
            self.dumber()
            self.special -= 1
        else: 
            if self.special > 0:
                print "%s uses %s \n(╯°Д°）╯︵ /(.□.\) %s rekt the %s!" % (self.name, self.specialname, self.name, self.enemy.name)
                self.do_maxdamage
                self.enemy = None
                self.state = 'normal' 
                self.knowledge += 1
                self.special -= 1
                print "%s feels smarter!" % self.name
            else: 
                print "%s is out of special skills!" % self.name
                self.enemy_argue()
    def enemy_argue(self):
        if self.enemy.do_damage(self):
            print "(╯°Д°）╯︵ /(.□.\) %s was rekt by the %s!!!\n %s heads home to join a fantasy football league in shame.\nPlease try again." %(self.name, self.enemy.name, self.name)
            play_again()

def play_again():
    raw_input("Would you like to play again? \nY/N?")
    if raw_input=="Y" or "y":
        print "Restart and run all cells to play again."
#        p=Player()
#        player_choice()
    else: print "have a great day"

def player_choice():
    choice=''
    while not (choice==1 or choice==2 or choice==3 or choice==4 or choice==5):
        try:
            choice = input("Oh, hello, I didn't see you there. You look smart as shit. I bet you're from Owl Town. \nWelcome back on campus. Did you hear the big protest rally is today? Are you here to protest?! \nSo which one are you, anyway? \nCorey? type 1 \nEric? press 2 \nJosh? press 3 \nKevin? press 4 \nParker? press 5")
        except NameError:
            print "\nNot an integer! Try again."
            continue 
    if choice==1:
        p.name='Corey'
        p.specialname='VERY ACCURATE THROW!'
    elif choice==2:
        p.name='Eric'
        p.specialname='PARTYING DAD!'
    elif choice==3:
        p.name='Josh'
        p.specialname='RETARD STRENGTH!'
    elif choice==4:
        p.name='Kevin'
        p.specialname='AVOIDS CONFRONTATION!'
    elif choice==5:
        p.name='Parker'
        p.specialname='SMARM!'
    print "\nWelcome, %s." % p.name

def player_choice_widget():
    print "Oh, hello, I didn't see you there. You look smart as shit. I bet you're from Owl Town. \nWelcome back on campus. Did you hear the big protest rally is today? Are you here to protest?! \nSo which one are you, anyway?"
    p.name=''
    value2=''
    while not (p.name=='Corey' or p.name=='Eric' or p.name=='Josh' or p.name=='Kevin' or p.name=='Parker'):
        w = widgets.ToggleButtons(options=['Corey', 'Eric', 'Josh', 'Kevin', 'Parker'], description="Choose:")
        display(w)
        value2 = input("Type 'Y' here after character is selected")
        continue
    w.value=p.name

journal = ["\n'Remember to check into off your habitica dailies.'\n", "'A Journal of My Habits and Goals.' -by Yours Truly.'"]
Feynman = ["\n'The sole test of the validity of any idea is experiment.'\n", "'Freshman Physics Lessons' -by Richard Feynman"]
Harris = ["\n'If someone doesnt value evidence, what evidence are you going to provide to prove that they should value it?'\n", "'Free Will' -by Sam Harris"]
Deutsch = ["\n'But one thing that all conceptions of the Enlightenment agree on is that it was a rebellion, and specifically a rebellion against authority in regard to knowledge.'\n", "'Beginning of Infinity' -by David Deutsch"]
Vonnegut = ["\n'Beware of the man who works hard to learn something, learns it, and finds himself no wiser than before. He is full of murderous resentment of people who are ignorant without having come by their ignorance the hard way.'\n", "'Cat\'s Cradle' -by Kurt Vonnegut"]
Sagan = ["\n'Smoke weed every day.'\n", "'Cosmos' -by Carl Sagan"]
#journalx = ["\nYou can't do that again, you've already read your journal today!", "'A Journal of My Habits and Goals.' -by Yours Truly.'"]
#playerbooks = [journal, None, None, None, None, None]
#bosslist=['Illiberal Professor', 'Fluid-gendered Women's Studies Major']
#book_list = [journal, Feynman, Harris, Deutsch, Vonnegut, Sagan]

book_dict = {
    "journal":("\n'Remember to check into my habitica today.'", "'A Journal of My Habits and Goals.' -by Yours Truly."), 
    "Feynman":("\n'The sole test of the validity of any idea is experiment.'", "'Freshman Physics Lessons' -by Richard Feynman"),
    "Harris":("\n'If someone doesnt value evidence, what evidence are you going to provide to prove that they should value it?'", "'Free Will' -by Sam Harris"),
    "Deutsch":("\n'But one thing that all conceptions of the Enlightenment agree on is that it was a rebellion, and specifically a rebellion against authority in regard to knowledge.'", "'Beginning of Infinity' -by David Deutsch"),
    "Vonnegut":("\n'Beware of the man who works hard to learn something, learns it, and finds himself no wiser than before. He is full of murderous resentment of people who are ignorant without having come by their ignorance the hard way.'", "'Cat\'s Cradle' -by Kurt Vonnegut"),
    "Sagan":("\n'Those afraid of the universe as it really is, those who pretend to nonexistent knowledge and envision a Cosmos centered on human beings will prefer the fleeting comforts of superstition.'", "'Cosmos'-by Carl Sagan'")}

Commands = {'help': Player.help, 'stats': Player.stats, 'read': Player.read,
  'explore': Player.explore, 'flee': Player.flee, 'argue': Player.argue, 'special': Player.special}

enemylist=['Marxist', 'Social Justice Warrior', 'Greenpeace Signature Gatherer']

p = Player()
player_choice()
print "\n(type 'help' to get a list of available actions!)\n"

while(p.knowledge < 16):
    line = raw_input("> ")
    args = line.split()
    if len(args) > 0:
        commandFound = False
        for c in Commands.keys():
            if args[0] == c[:len(args[0])]:
                Commands[c](p)
                commandFound = True
                break
        if not commandFound:
            print "%s doesn't understand the suggestion." % p.name
    elif args==q or quit:
        print "Thanks for playing."
print "%s vanquished all the post-modernist illiberals! %s has returned freedom of speach to campus! \n ┻━┻ ︵¯\(ツ)/¯ ︵ ┻━┻" %(p.name, p.name)
