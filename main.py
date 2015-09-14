import random
import math

#
#   Constants
#
STARTING_SUPPLIES = 7
STARTING_MEDICINE = 0
STARTING_DEFENSE = 3
STARTING_DANGER = 1

class Game:
    #
    #   Game Setup
    #
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = self.make_players()
        self.monsters = random.choice(['zombies', 'zombies', 'zombies', 'vampires', 'werewolves', 'ghosts', 'pop star fangirls'])
        self.base = self.make_base()
        self.day = 0

    #
    #   Creates player objects based on self.player_count
    #
    def make_players(self):
        players = []
        for i in range(self.player_count):
            name = ''
            while name == '':
                name = raw_input('Enter name for Player ' + str(i+1) + ': ')
            player = Player(name, self)
            players.append(player)
        return players

    #
    #   Creates a Base object
    #
    def make_base(self):
        names = ['underground bunker', 'cabin lodge', 'penthouse suite', 'backstage VIP lounge']
        return Base(random.choice(names), self.player_count, self)

    #
    #   Splits players into sorted groups
    #
    def split_players(self, group_count):
        groups = []

        for i in range(group_count):
            groups.append([])

        for i in range(len(self.players)):
            groups[random.randint(0,group_count-1)].append(self.players[i])

        return groups

    #
    #   Returns a list of players like so: 'A, B and C'
    #
    def build_name_list(self, players):
        s = ''
        l = len(players)
        for i in range(l):
            s += players[i].name
            if i < l - 2:
                s += ', '
            elif i < l - 1:
                s += ' and '
        return s

    #
    #   Start the game
    #
    def play(self):
        groups = self.split_players(2)
        s = '\nNone of us expected the apocalypse to happen. Not here. Not now.\n'
        s += 'Not with ' + self.monsters + '.\nBut it totally did.\n\n'

        group1 = self.build_name_list(groups[0])
        group2 = self.build_name_list(groups[1])

        if group1 != '' and group2 != '':
            s += group1 + ' made it to the ' + self.base.name + ' first.\n'
            s += 'Over the next few days, ' + group2 + ' showed up at the base.\n\n'
        elif group1 != '':
            s += group1 + ' made it to the ' + self.base.name + ' first.\n'
            s += 'They waited for other survivors ... but no one ever showed.\n\n'
        else:
            s += 'The ' + self.base.name + ' was left untouched for the first few days.\n'
            s += 'Over the next few days, ' + group2 + ' showed up at the base.\n\n'

        for i in range(len(groups[0])):
            p = groups[0][i]
            t = p.pick_starting_trait()
            if t == 'injured':
                s += p.name + ' has been injured for a few days now, but shows no signs of infection.\n'
            elif t == 'infected':
                s += p.name + ' has been injured for a few days now, and doesn\'t seem to be getting any better.\n'

        for i in range(len(groups[1])):
            p = groups[1][i]
            t = p.pick_starting_trait()
            if t == 'injured' or t == 'infected':
                s += p.name + ' looked hurt pretty badly, but we let them in anyway.\n'

        s += '\nThere are ' + str(self.player_count) + ' of us in total.\n'
        s += 'We have about ' + str(self.base.supplies) + \
             ' days of food and water for all of us ... but we\'ll need to forage soon.\n'
        s += 'Our defenses will only hold for ' + str(self.base.defense) + \
             ' more nights. We should shore them up right away.\n'

        print s
        raw_input('Press enter to continue...\n')
        self.next_day()

    #
    #   Advance to the next day in the game
    #
    def next_day(self):
        self.day += 1

        # Check if game over
        if self.base.population == 0:
            print '----- GAME OVER -----'
            print 'Everyone is either dead or ' + self.monsters + '.'
            print 'You survived a total ' + str(self.day) + ' days.'
            return

        # Status reports
        print '----- DAY ' + str(self.day) + ' -----'
        self.base.status_report()
        for player in self.players:
            if player.alive:
                print player.status_report()

        raw_input('\nPress enter to continue...\n')

        # Take turns for each player
        for player in self.players:
            if player.alive:
                player.take_turn()

        # Night time
        print 'The sun sits low in the sky, and we all gather together inside the ' + self.base.name\
              + ' to wait for nightfall...'

        self.base.consume_supplies()
        raw_input('\nPress enter to continue...\n')

        self.next_day()


class Player:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.alive = True
        self.rested = False
        self.hungry = False
        self.injured = False
        self.infected = False
        self.infected_days = 0
        self.traits = []

    #
    #   Assigns a random starting trait to the survivor and returns its name
    #
    def pick_starting_trait(self):
        traits = ['injured', 'untrusted', 'trusted', 'lifesaver', 'calm', 'paranoid', 'pragmatic', 'violent', 'infected']
        t = random.choice(traits)
        if t == 'infected':
            self.injured = True
            self.infected = True
        elif t == 'injured':
            self.injured = True
        else:
            self.traits.append(t)
        return t

    #
    #   Processes a turn for the character (player's choice)
    #
    def take_turn(self):
        print '\n----- ' + self.name.upper() + ' -----'

        self.check_infection()
        choice = ''
        if not self.injured:
            choices = ['Scavenge for supplies',
                       'Fortify base',
                       'Hunt nearby ' + self.game.monsters,
                       'Keep watch',
                       'Get some rest']
            while choice not in ['1', '2', '3', '4', '5']:
                for i in range(len(choices)):
                    print str(i+1) + '. ' + choices[i]
                choice = raw_input('\nWhat should ' + self.name + ' do today? (Enter a number.)\n')
            self.perform_action(choices[int(choice)-1])
        else:
            # Attempt to resolve injury
            recovery_chance = 33
            if self.game.base.medicine > 0:
                print self.name + ' took some medicine.'
                recovery_chance = 66

            if random.randint(0, 100) <= recovery_chance:
                self.injured = False
                print self.name + ' is looking better today. They can probably help again tomorrow.'
            else:
                print self.name + ' doesn\'t look much better today.'

            raw_input('\nPress enter to continue...\n')

    #
    #   Removes player from the game
    #
    def die(self):
        self.alive = False
        self.game.base.population -= 1

    #
    #   Increments infection if necessary
    #
    def check_infection(self):
        if self.infected:
            self.infected_days += 1
        if self.infected_days > 9:
            print self.name + ' has succumbed to the infection. There was nothing more we could do.'
            self.die()

    #
    #   Performs and returns the result of a player's choice during a turn
    #
    def perform_action(self, action):
        action_roll = random.randint(0, 100)
        infection_roll = random.randint(0, 100)
        if self.rested:
            self.rested = False
            action_roll += 10
        if self.hungry:
            self.hungry = False
            action_roll -= 15

        if action == 'Scavenge for supplies':
            if action_roll > 75:
                self.game.base.supplies += random.randint(1, 3)
                self.game.base.medicine += random.randint(1, 2)
                result = self.name + ' brought back some medicine from the pharmacy.'
            elif action_roll > 25:
                self.game.base.supplies += random.randint(1, 3)
                result = self.name + ' brought back a random assortment of supplies from town.'
            elif action_roll > 10:
                result = self.name + ' couldn\'t find anything useful while scavenging.'
            else:
                self.injured = True
                if infection_roll < 20:
                    self.infected = True
                result = self.name + ' was injured while looking for supplies.'
        elif action == 'Fortify base':
            if action_roll > 25:
                self.game.base.defense += random.randint(1, 3)
                result = self.name + ' made some improvements to the base.'
            else:
                result = self.name + ' didn\'t get much done around the base today.'
        elif action == 'Keep watch':
            if action_roll > 25 and self.game.base.danger > 1:
                self.game.base.danger -= 1
                result = self.name + ' kept watch all day and took out a few ' + self.game.monsters + '.'
            else:
                result = self.name + ' kept watch all day, but nothing came by.'
        elif action == 'Get some rest':
            self.rested = True
            result = self.name + ' stayed in today and tried to relax.'
        else:
            if action_roll > 15:
                result = self.name + ' took out a group of ' + self.game.monsters + ' wandering close to the base.'
            elif action_roll > 5:
                self.injured = True
                if infection_roll < 20:
                    self.infected = True
                result = self.name + ' was injured while trying to kill ' + self.game.monsters + ' around the base.'
            else:
                result = self.name + ' went out to kill ' + self.game.monsters + ' ... but they didn\'t come back.'
                self.die()

        print result
        raw_input('\nPress enter to continue...\n')

    #
    #  Returns a (mostly useless) string about how the character is doing
    #
    def status_report(self):
        reports = [' seems calm today.',
                   ' seems nervous today.',
                   ' seems anxious today.',
                   ' is trying not to cry.',
                   ' is unsure what to do.',
                   ' wants to get to the action.',
                   ' is ready to go.']
        message = ''
        if self.injured:
            message += self.name + ' is injured and can\'t do anything today. '
        if self.infected:
            if self.infected_days < 3:
                message += self.name + ' is looking unwell. '
            elif self.infected_days < 6:
                message += self.name + ' is looking badly ill. '
            else:
                message += self.name + ' looks close to turning. '
        if not self.injured and not self.infected:
            if 'untrusted' in self.traits:
                reports.append(' is looking suspicious today.')
            if 'trusted' in self.traits:
                reports.append(' will guide the group to safety.')
            if 'lifesaver' in self.traits:
                reports.append(' is keeping an eye out for others.')
                reports.append(' has your back today.')
            if 'calm' in self.traits:
                reports.append(' waits patiently to hear the day\'s plan.')
            if 'paranoid' in self.traits:
                reports.append(' looks at you suspiciously. "Now what?"')
            if 'pragmatic' in self.traits:
                reports.append(' is already preparing for another outing.')
            if 'violent' in self.traits:
                reports.append(' waits by the door, ready to kill.')
            message += self.name + random.choice(reports)
        return message


class Base:
    def __init__(self, name, player_count, game):
        self.name = name
        self.population = player_count
        self.game = game
        self.supplies = 7
        self.medicine = 0
        self.defense = 3
        self.danger = 1

    def status_report(self):
        print 'There are ' + str(self.population) + ' of us left.'
        print 'We have ' + str(self.supplies) + ' days of food and water.'
        print 'We have ' + str(self.medicine) + ' medicine in stock.'
        print 'Our defenses will hold for ' + str(int(math.floor(self.defense / self.danger))) + ' more nights.' +\
              ' (' + str(self.defense) + ' defense / ' + str(self.danger) + ' danger)\n'

    def consume_supplies(self):
        self.supplies -= 1
        self.defense -= self.danger

        danger_roll = random.randint(0, 100)

        if danger_roll > 50:
            self.danger += 1
            print 'The horde of ' + self.game.monsters + ' is getting thicker ...'

        if self.defense <= 0:
            self.defense = 0
            print 'The ' + self.game.monsters + ' broke through our defenses tonight.'
            for i in range(random.randint(0, 2)):
                p = random.choice(self.game.players)
                if p.alive and not p.injured:
                    p.injured = True
                    print p.name + ' was injured in the attack.'
            p = random.choice(self.game.players)
            if p.alive:
                print p.name + ' didn\'t make it in the attack.'
                p.die()
        else:
            print 'The defenses held tonight.'

        if self.supplies <= 0:
            self.supplies = 0
            print 'Some of us couldn\'t eat tonight.'
            for i in range(random.randint(0, 2)):
                p = random.choice(self.game.players)
                if p.alive:
                    p.hungry = True
                    print p.name + ' didn\'t even get scraps.'
            p = random.choice(self.game.players)
            if p.alive:
                print p.name + ' struck out on their own. "Better to die out there than starve in here."'
                p.die()
        else:
            print 'We had enough for everyone to eat tonight.'


def main():
    print '----- HELLO APOCALYPSE -----'
    print 'Welcome to Hello Apocalypse!'
    players = ''
    while players not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        players = raw_input('How many people are playing? (1-10) ')
    Game(int(players)).play()

main()
