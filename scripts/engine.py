"""One game session, with no terminal or browser dependencies.

Call start() once, then submit() once per command or menu choice. Results contain
only JSON-compatible data; rendering, delays, and process exit belong to adapters.
"""

from scripts.classes import BOOK_CHOICES, Commands, Boss, Player, PlayerDict


class Game:
    TERMINAL_PHASES = ('won', 'lost', 'quit')

    def __init__(self, rng=None):
        self._messages = []
        self.player = Player(rng=rng, emit=self._emit)
        self.boss = None
        self._phase = 'character_selection'
        self._started = False

    def _emit(self, message):
        self._messages.append(message)

    @property
    def phase(self):
        if self._phase == 'character_selection' or self._phase in self.TERMINAL_PHASES:
            return self._phase
        if self.player.state == 'book_choice':
            return 'book_selection'
        if self.player.state == 'argue':
            return 'boss_combat' if self.player.enemy is self.boss else 'combat'
        return 'exploration'

    def start(self):
        """Return the introduction; calling again does not restart the session."""
        self._messages = []
        if not self._started:
            self._started = True
            self._emit(
                "Oh, hello, I didn't see you there. You look smart as shit. I bet you're from Owl Town and"
                "\nback on campus for some learning. Well watch out for the big rally today planned over in Red Square.")
            self._emit("..........."
                       "\nSo which one are you, anyway?"
                       "\nCorey? type 1 \nEric? press 2 \nJosh? press 3 \nKevin? press 4 \nParker? press 5")
        return self._result()

    def submit(self, text):
        """Resolve a command or pending choice and return this turn's result."""
        if not self._started:
            raise RuntimeError('Call start() before submitting actions.')
        self._messages = []
        if self.phase in self.TERMINAL_PHASES:
            return self._result()

        command = ' '.join(text.lower().split())
        if command in ('q', 'quit'):
            self.player.quit()
            self._phase = 'quit'
        elif self.phase == 'character_selection':
            self._choose_character(command)
        elif self.phase == 'book_selection':
            self.player.choose_book(command)
        else:
            self._dispatch(command)
        return self._result()

    def _choose_character(self, choice):
        character = PlayerDict.get('P' + choice)
        if character is None:
            self._emit('Please choose a character from 1 to 5.')
            return
        self.player.name, self.player.specialname = character
        self._phase = 'exploration'
        self._emit("\nWelcome, {}. (type help to see what your options are)".format(self.player.name))

    def _dispatch(self, command):
        if not command:
            return
        matches = [name for name in Commands if name.startswith(command)]
        if len(matches) != 1:
            self._emit("{} doesn't understand the suggestion.".format(self.player.name))
            return
        name = matches[0]
        previous_enemy = self.player.enemy
        if name == 'explore' and self.boss is not None and self.player.state == 'normal':
            # Escaping is not victory; the next exploration resumes the same boss.
            self._enter_boss()
        else:
            Commands[name](self.player)
        self._resolve_outcome(previous_enemy)

    def _resolve_outcome(self, previous_enemy):
        if self.player.knowledge <= 0:
            self._phase = 'lost'
            self._emit(
                "Your head feels a little foggy, but you can't think of any response. Maybe you will go home and nap. "
                "\nPlease reload the program to play again.")
        elif self.player.state == 'quit':
            self._phase = 'quit'
        elif self.boss is not None and previous_enemy is self.boss and self.boss.knowledge <= 0:
            self._phase = 'won'
            self._win_messages()
        elif self.boss is None and self.player.knowledge >= 16 and self.player.state == 'normal':
            self._enter_boss()

    def _enter_boss(self):
        if self.boss is None:
            self.boss = Boss(rng=self.player.rng, emit=self._emit)
        self.player.state = 'argue'
        self.player.enemy = self.boss
        self._emit(
            "-----------FINAL STAGE------------\n {} joins the free speech rally. "
            "But what is this?! An angry mob wants to de-platform the rally! {} wonders what they're afraid of hearing?"
            " \nBOSS ENCOUNTERED \n {} encounters the {}!".format(
                self.player.name, self.player.name, self.player.name, self.boss.name))
        self._emit(
            "\n 'You think we care about OBJECTIVE TRUTH and KNOWLEDGE?!"
            " We only believe in the subjective truths our LIVED EXPERIENCES!"
            " What can you possibly say to deny this??', says the {}".format(self.boss.name))

    def _win_messages(self):
        self._emit(
            "\n {} vanquished all the post-modernist illiberals! {} has returned freedom of speech to campus! \n".format(
                self.player.name, self.player.name))
        self._emit(
            "Hi, this is ReKrap, and thanks for playing. I know we had a lot of fun today, but its important to remember "
            "that knowledge is half the battle thumbs up emoji")
        self._emit('developer - ReKrap')
        self._emit('writer - ReKrap')
        self._emit('THE END')
        self._emit("P.S. There's a potential Donkey Kong kill screen coming up if anyone is interested.")

    def _result(self):
        phase = self.phase
        if phase == 'character_selection':
            choices = [{'value': key[1:], 'label': value[0]} for key, value in PlayerDict.items()]
            prompt = 'Choice ='
        elif phase == 'book_selection':
            choices = [{'value': key, 'label': value[1]} for key, value in BOOK_CHOICES.items()]
            choices.append({'value': '0', 'label': 'Leave without a book'})
            prompt = 'Book choice ='
        elif phase in self.TERMINAL_PHASES:
            choices = []
            prompt = None
        else:
            choices = [{'value': command, 'label': command} for command in Commands]
            prompt = 'What would you like to do? > '
        enemy = self.player.enemy
        return {
            'messages': list(self._messages),
            'phase': phase,
            'prompt': prompt,
            'choices': choices,
            'finished': phase in self.TERMINAL_PHASES,
            'state': {
                'player': {
                    'name': self.player.name,
                    'knowledge': self.player.knowledge,
                    'knowledge_max': self.player.knowledge_max,
                    'special_charges': self.player.special_charges,
                    'specialname': self.player.specialname,
                    'books': [{'title': book[1], 'passage': book[0]} for book in self.player.playerbooks],
                },
                'enemy': {'name': enemy.name, 'knowledge': enemy.knowledge} if enemy is not None else None,
            },
        }
