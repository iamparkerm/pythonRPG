from random import randint
import random

# this version is python 2!
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
            print "%s counters %s's argument!" % (enemy.name, self.name)
        else: 
            print "%s's argument hurts %s's feelings!" % (self.name, enemy.name)
            print "%s: knowledge = %d" % (enemy.name, enemy.knowledge)
        return enemy.knowledge <= 0
        print "enemy's knowledge just returned <=0"
    def do_maxdamage(self, enemy):
        enemy.knowledge=0
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
        print random.choice(enemy_quote)
        
class Boss(Enemy):
    def __init__(self):
        Character.__init__(self)
        self.name = 'Marxist Professor'
        self.knowledge = 20
#    def special(self):
#        do_damage(enemy) * 2
        
class Player(Character):
    def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.knowledge = 7
        self.knowledge_max = 8
        self.books = 1
        self.playerbooks = [journal, None, None, None, None, None]
    def help(self): print Commands.keys()
    def stats(self): print "%s's knowledge: %d/%d special: %d book(s): %d" % (self.name, self.knowledge, self.knowledge_max, self.special, self.books)
    def dumber(self):
        if self.knowledge == 1:
            pass
        else:
            print "%s feels a little dumber now." % self.name
            self.knowledge -= 1
    def backpack(self):
        if self.playerbooks[0]:
            print self.playerbooks[0][1]
        if self.playerbooks[1]:
            print self.playerbooks[1][1]
        if self.playerbooks[2]:
            print self.playerbooks[2][1]
        if self.playerbooks[3]:
            print self.playerbooks[3][1]
        if self.playerbooks[4]:
            print self.playerbooks[4][1]
        if self.playerbooks[5]:
            print self.playerbooks[5][1]
        else:
            print "%s's backpack is empty." % self.name
    def read_book(self):
        if Sagan in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Sagan)][1]), self.playerbooks[self.playerbooks.index(Sagan)][0]
            self.playerbooks.remove(Sagan)
            self.playerbooks.insert(5, None)
            self.books -=1
        elif Vonnegut in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Vonnegut)][1]), self.playerbooks[self.playerbooks.index(Vonnegut)][0]
            self.playerbooks.remove(Vonnegut)
            self.playerbooks.insert(4, None)
            self.books -=1
        elif Deutsch in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Deutsch)][1]), self.playerbooks[self.playerbooks.index(Deutsch)][0]
            self.playerbooks.remove(Deutsch)
            self.playerbooks.insert(3, None)
            self.books -=1
        elif Harris in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Harris)][1]), self.playerbooks[self.playerbooks.index(Harris)][0]
            self.playerbooks.remove(Harris)
            self.playerbooks.insert(2, None)
            self.books -=1
        elif Feynman in self.playerbooks:
            print "%s takes out a book and reads a passage from %s: \n" % (self.name, self.playerbooks[self.playerbooks.index(Feynman)][1]), self.playerbooks[self.playerbooks.index(Feynman)][0]
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
                print "%s encounters a %s! The %s shrieks:" % (self.name, self.enemy.name, self.enemy.name)
                self.enemy.quote()
                self.state = 'argue'
            else:
                if randint(0,1):
                    print "%s finds a flyer pointing him towards today's big free speach rally and corrects his course." % self.name
                else:
                    if randint(0, 1):
                        print "%s stumbles upon a library! Choose a book from the below shelf to take with you:" % self.name
                        new_book = input("\nCarl Sagan? type 1 \nKurt Vonnegut? press 2 \nDavid Deutsch? press 3 \nSam Harris? press 4 \nRichard Feynman? press 5")                   
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
                    else:
                        if randint(0, 1):
                            print "Oops, %s realized he just walked in a circle..." % self.name
                            self.dumber()
                        else: print "%s ventures further toward the liberal arts halls." % self.name
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
                print "%s couldn't escape from the %s! (?'?')?? ???" % (self.name, self.enemy.name)
                self.enemy_argue()
    def argue(self):
        if self.state != 'argue': 
            print "%s orates into the air at no one in particular. No one takes the bait." % self.name
        else:
            if self.do_damage(self.enemy):
                print "%s vanquishes the %s! (?°?°)?? /(.O.\) " % (self.name, self.enemy.name)
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
                print "%s uses %s \n(?°?°)?? /(.?.\) \n %s rekt the %s!" % (self.name, self.specialname, self.name, self.enemy.name)
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
            print "(?°?°)?? /(.?.\) %s was rekt by the %s!!!\n %s heads home to join a fantasy football league in shame.\nPlease try again." %(self.name, self.enemy.name, self.name)

def player_choice():
    choice=''
    while not (choice==1 or choice==2 or choice==3 or choice==4 or choice==5):
        try:
            choice = input("Oh, hello, I didn't see you there. You look smart as shit. I bet you're from Owl Town. \nWelcome back on campus. Did you hear the big rally is today? Are you here to protest?! \nSo which one are you, anyway? \nCorey? type 1 \nEric? press 2 \nJosh? press 3 \nKevin? press 4 \nParker? press 5")
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

def kill_screen():
    print "\n %s vanquished all the post-modernist illiberals! %s has returned freedom of speech to campus! \n  ????? ¯\(?)/¯ ?????" %(p.name, p.name)
    print "Hi, this is ReKrap, and thanks for playing today."
    print "developer - ReKrap"
    print "writer - ReKrap"
    print "THE END"
    print "P.S. There's a potential Donkey Kong kill screen coming up if anyone is interested."
def killed_screen():
    print "\nPlease reload the page/kernel to play again."

enemy_quote  = [" 'Gender is a social construct!' ", " 'You are oppressing our safe spaces!' ", " '*snap*! *snap*! *snap*! *snap*!' ", " 'You're appropriating my culture!' ", "'Look it's a member of the patriarchy!'", "'I find my priviledges more virtuous than yours!'"]
journal = ["\n'Remember to check off your habitica dailies.'\n", "'A Journal of My Habits and Goals.' -by Yours Truly"]
Feynman = ["\n'The sole test of the validity of any idea is experiment.'\n", "'Freshman Physics Lessons' -by Richard Feynman"]
Harris = ["\n'If someone doesnt value evidence, what evidence are you going to provide to prove that they should value it?'\n", "'Free Will' -by Sam Harris"]
Deutsch = ["\n'But one thing that all conceptions of the Enlightenment agree on is that it was a rebellion, and specifically a rebellion against authority in regard to knowledge.'\n", "'Beginning of Infinity' -by David Deutsch"]
Vonnegut = ["\n'Beware of the man who works hard to learn something, learns it, and finds himself no wiser than before. He is full of murderous resentment of people who are ignorant without having come by their ignorance the hard way.'\n", "'Cat\'s Cradle' -by Kurt Vonnegut"]
Sagan = ["\n'Smoke weed every day.'\n", "'Cosmos' -by Carl Sagan"]

Commands = {'help': Player.help, 'stats': Player.stats, 'read': Player.read,
  'explore': Player.explore, 'flee': Player.flee, 'argue': Player.argue, 'special': Player.special, 'backpack': Player.backpack}

enemylist=['Social Justice Warrior', 'Greenpeace Signature Gatherer', 'White Knight']

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
    if p.knowledge == 0:
        killed_screen()
        break

boss = Boss()
p.state = 'argue'
p.enemy = boss
print "-----------------------\n %s finally finds the free speach rally. But what is this?! An angry mob wants to silence the rally! %s wonders what they're afraid of hearing? \nBOSS ENCOUNTERED \n %s encounters a %s!" % (p.name, p.name, p.name, boss.name)
print "\n 'You think we care about OBJECTIVE TRUTH and KNOWLEDGE?! We only believe in the subjective truths our LIVED EXPERIENCES! Now prepare to argue...', says the %s" % boss.name

while(boss.knowledge>0):
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
            print "%s doesn't understand the suggestion."
    if p.state != 'argue':
        kill_screen()
        break
