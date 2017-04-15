import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
app.config['ASK_VERIFY_REQUESTS'] = False
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

class Messages():
    def welcome_msg(self):
        msg = 'Welcome to "I am a Pokemon!" game!'\
              'Choose an avatar! Bulbasaur, Charmander, '\
              'Squirtle or Pikachu! You can just say the pokemon\'s name'\
              'or say "I choose you Pikachu"'
        return msg

    def intro_want_to_play(self):
        msg = 'So you have a pokemon now but it\'s at level 0 now.'\
              'Play small games with your pokemon to level it up'
        return msg

    def i_have_a_number_in_mind(self, lower, upper):
        msg = 'I have a number in mind, from the range {0} to {1},'\
                    'Can you guess the number?'.format(lower, upper)
        return msg

    def random_number_game_plays_exceeded(self):
        msg = 'Sorry you can only play this game 5 times a day!'\
              'You need to wait 24hours to play again'
        return msg

    def success_msg(self):
        msgs = [
                'Wow you did it! Really awesome',
                'Yepp! This is the correct answer',
                'Exactly, right, you are a genius'
            ]
        return msgs(randint(0,len(msgs)))

    def fail_msg(self):
        msgs = [
                'Sorry, this is wrong!',
                'You have failed me',
                'Wrong answer'
            ]
        return fail_msg

    def play_again(self):
        msg = 'Want to try again?'
        return msg

msg = Messages()

def pokemon_jsoner(pokeobj):
    dic = {}
    dic["name"] = pokeobj.name
    dic["make_name_sound"] = pokeobj.make_name_sound()
    dic["level"] = pokeobj.level
    return dic

class Pokemon(object):
    def __init__(self, name, name_sounds):
        self.name = name
        self.moves = []
        self.level = 0
        self.name_sounds = name_sounds

    def make_name_sound(self):
        # sound_no = randint(0,len(self.name_sounds)-1)
        # msg = self.name_sounds[sound_no]
        return self.name_sounds

    def level_up(self):
        if self.level == 100:
            return ('You are already at highest level 100!')
        self.level += 1
        msg = 'Congrats! You have reached level!'
        return (msg + '. '+ self.level)

class Bulbasaur(Pokemon):
    name_sounds = [
            'Buba bulbasaur',
            'buba buba bulllbasaur',
            'bulbasaur bulbasaur',
            'bulba bulbasaur'
        ]
    def __init__(self):
        super(Bulbasaur, self).__init__('bulbasaur', self.name_sounds)
        # super(Bulbasaur, self).__init__()
        #'Bulbasaur',name_sounds) 

class Charmander(Pokemon):
    def __init__(self):
        name_sounds = [
                'Char Charmander',
                'Charmnder Charmnder',
                'Chari Chari Mender',
                'Charmander Charmander'
            ]
        super(Charmander, self).__init__('Charmander', name_sounds)

class Squirtle(Pokemon):
    def __init__(self):
        name_sounds = [
                'Squirtle Squirtle',
                'Squirt Squirt Turtle',
                'Squirtle Squirtle',
                'Squirtle Squirtle Squirtle Squirtle!'
            ]
        super(Squirtle, self).__init__('Squirtle', name_sounds)

class Pikachu(Pokemon):
    def __init__(self):
        name_sounds = [
                'Pika Pika Pikachu!',
                'Pikaaaachhhu!!',
                'Pika Pika!',
                'Pikachu!! Pikachu!!'
            ]
        super(Pikachu, self).__init__('Pikachu', name_sounds)

@ask.launch
def new_game():
    welcome_msg = msg.welcome_msg()
    return question(welcome_msg)

@ask.intent("BeginJourneyChoiceIntent")
def begin_journey(choice):
    print('The choice is : {}'.format(choice))
    choice = choice.lower()
    if choice == 'bulbasaur':
        pokemon = Bulbasaur()
    elif choice == 'charmander':
        pokemon = Charmander()
    elif choice == 'squirtle':
        pokemon = Squirtle()
    elif choice == 'pikachu':
        pokemon = Pikachu()
    intro_want_to_play = msg.intro_want_to_play()
    session.attributes['pokemon'] = pokemon_jsoner(pokemon)
    return question(intro_want_to_play)

@ask.intent('PlayAGameIntent')
def play_game():
    if 'random_number_game_plays' not in session.attributes:
        print('not in dict')
        session.attributes['random_number_game_plays'] = 0
    else:
        if session.attributes['random_number_game_plays'] == 5:
            random_number_game_plays_exceeded_msg = \
                    msg.random_number_game_plays_exceeded()
            return question(random_number_game_plays_exceeded_msg)
        session.attributes['random_number_game_plays'] += 1
    base = randint(0,9)
    length = randint(1,5)
    ceil = base + length
    random_number_range = [i for i in range(base, ceil+1)]
    random_number = randint(base, ceil)
    session.attributes['random'] = random_number
    i_have_a_number_in_mind_msg = msg.i_have_a_number_in_mind(base, ceil)
    print('Random number is ', random_number)
    print('TEXT HERE: ', i_have_a_number_in_mind_msg)
    return question(i_have_a_number_in_mind_msg)

@ask.intent("NoIntent")
def leave_gracefully():
    return statement('losers are quitters, spread salt on your sorry buttocks man')

@ask.intent("RandomNumberIntent", convert={'num': int})
def choice(num):
    session.attributes['random_number_game_plays'] += 1
    if num==session.attributes['random']:
        success_msg = msg.success_msg()
        play_again_msg = msg.play_again()
        session.attributes['pokemon'].level += 1
        return question(success_msg+'. '+level_up_msg+'. '+play_again_msg)
    else:
        fail_msg = msg.fail_msg()
        play_again_msg = msg.play_again()
        return question(fail_msg+'. '+play_again_msg)
    
@ask.intent('MyLevelIntent')
def my_level():
    msg = session.attributes['pokemon'].level
    return question(msg)

@ask.intent("HelloPokemonIntent")
def hello_pokemon():
    name_sounds = session.attributes['pokemon'].make_name_sound
    return name_sounds(randint(0,len(name_sounds)-1))

if __name__ == '__main__':
    app.run(debug=True)
