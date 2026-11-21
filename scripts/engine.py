"""Run one turn at a time. Terminal and browser interfaces display the messages."""

from scripts.classes import Commands, Boss, Player, PlayerDict


class Game:
    def __init__(self, rng=None):
        self.messages = []
        self.player = Player(rng=rng, emit=self.messages.append)
        self.boss = None
        self.phase = 'character_selection'

    @property
    def finished(self):
        return self.phase in ('won', 'lost', 'quit')

    @property
    def prompt(self):
        if self.phase == 'character_selection':
            return 'Choice ='
        if self.phase == 'book_selection':
            return 'Book choice ='
        return 'What would you like to do? > '

    def start(self):
        return [
            "Oh, hello, I didn't see you there. You look smart as shit. I bet you're from Owl Town and"
            "\nback on campus for some learning. Well watch out for the big rally today planned over in Red Square.",
            "..........."
            "\nSo which one are you, anyway?"
            "\nCorey? type 1 \nEric? press 2 \nJosh? press 3 \nKevin? press 4 \nParker? press 5",
        ]

    def submit(self, text):
        self.messages.clear()
        if self.finished:
            return []
        command = ' '.join(text.lower().split())

        if command in ('q', 'quit'):
            self.phase = 'quit'
        elif self.phase == 'character_selection':
            character = PlayerDict.get('P' + command)
            if character:
                self.player.name, self.player.specialname = character
                self.phase = 'exploration'
                self.messages.append("\nWelcome, {}. (type help to see what your options are)".format(self.player.name))
            else:
                self.messages.append('Please choose a character from 1 to 5.')
        else:
            if self.phase == 'book_selection':
                self.player.choose_book(command)
            elif command:
                self._dispatch(command)
            self._resolve_outcome()
        return self.messages[:]

    def _dispatch(self, command):
        for name, action in Commands.items():
            if name.startswith(command):
                if name == 'explore' and self.boss and self.player.state == 'normal':
                    self._enter_boss()
                else:
                    action(self.player)
                return
        self.messages.append("{} doesn't understand the suggestion.".format(self.player.name))

    def _resolve_outcome(self):
        if self.player.knowledge <= 0:
            self.phase = 'lost'
            self.messages.append(
                "Your head feels a little foggy, but you can't think of any response. Maybe you will go home and nap. "
                "\nPlease reload the program to play again.")
        elif self.player.state == 'quit':
            self.phase = 'quit'
        elif self.boss and self.boss.knowledge <= 0:
            self.phase = 'won'
            self._win_messages()
        elif self.player.state == 'book_choice':
            self.phase = 'book_selection'
        elif self.player.state == 'argue':
            self.phase = 'boss_combat' if self.player.enemy is self.boss else 'combat'
        else:
            self.phase = 'exploration'
            if self.boss is None and self.player.knowledge >= 16:
                self._enter_boss()

    def _enter_boss(self):
        # After escape, reuse the same boss instead of declaring victory.
        if self.boss is None:
            self.boss = Boss(rng=self.player.rng, emit=self.messages.append)
        self.player.state = 'argue'
        self.player.enemy = self.boss
        self.phase = 'boss_combat'
        self.messages.append(
            "-----------FINAL STAGE------------\n {} joins the free speech rally. "
            "But what is this?! An angry mob wants to de-platform the rally! {} wonders what they're afraid of hearing?"
            " \nBOSS ENCOUNTERED \n {} encounters the {}!".format(
                self.player.name, self.player.name, self.player.name, self.boss.name))
        self.messages.append(
            "\n 'You think we care about OBJECTIVE TRUTH and KNOWLEDGE?!"
            " We only believe in the subjective truths our LIVED EXPERIENCES!"
            " What can you possibly say to deny this??', says the {}".format(self.boss.name))

    def _win_messages(self):
        self.messages.extend([
            "\n {} vanquished all the post-modernist illiberals! {} has returned freedom of speech to campus! \n".format(
                self.player.name, self.player.name),
            "Hi, this is ReKrap, and thanks for playing. I know we had a lot of fun today, but its important to remember "
            "that knowledge is half the battle thumbs up emoji",
            'developer - ReKrap',
            'writer - ReKrap',
            'THE END',
            "P.S. There's a potential Donkey Kong kill screen coming up if anyone is interested.",
        ])
