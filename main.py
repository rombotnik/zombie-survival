import random

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

    def make_players(self):
        players = []
        for i in range(self.player_count):
            name = input('Enter name for Player ' + str(i+1) + ':')
            player = Player(name, self)
            players.append(player)
        return players

    def make_base(self):
        names = ['Underground Bunker', 'Cabin Lodge', 'Penthouse Apartment', 'Backstage VIP Lounge']
        return Base(random.choice(names), self.player_count)

    #
    #   Utility functions
    #
    def split_players(self, group_count):
        groups = []

        for i in range(group_count):
            groups.append([])

        for i in range(len(self.players)):
            groups[random.randint(0,group_count-1)].append(self.players[i])

        return groups

    def build_name_list(self, names):
        s = ''
        l = len(names)
        for i in range(l):
            s += names[i]
            if i < l - 2:
                s += ', '
            elif i < l - 1:
                s += ', and '
        return s

    def play(self):
        groups = self.split_players(2)
        s = 'None of us expected the apocalypse to happen. Not here. Not now.\n'
        s += 'Not with ' + self.monsters + '.\nBut it totally did.\n'
        s += self.build_name_list(groups[0]) + ' made it to the ' + self.base.name + ' first. '
        s += 'They barred the doors and waited with baited breath ... but nothing came for them.\n'
        s += 'Over the next few days, ' + self.build_name_list(groups[1]) + ' showed up at the base.\n\n'

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

        s += '\nThere are ' + self.player_count + ' in total. '
        s += 'We have about 30 days of food and water for all of us ... but we\'ll need to forage soon.\n'
        s += 'Our defenses will only hold for 3 more nights. We should shore them up right away.'

        print s
        input('Press enter to continue...')
        self.next_day()

    # Advances to the next day in the game and prompts the player to make decisions
    def next_day(self):
        self.day += 1

        # Status reports
        print '----- DAY ' + str(self.day) + ' -----'


        for player in self.players:
            if player.alive:
                print player.status_report()

        for player in self.players:
            if player.alive and not player.injured:
                player.take_turn()

class Player:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.alive = True
        self.rested = False
        self.injured = False
        self.infected = False
        self.infected_days = 0
        self.traits = []

    # Assigns a random starting trait to the survivor and returns its name
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

    # Processes a turn for the character
    def take_turn(self):
        print '----- ' + self.name.upper() + ' -----'

        if not self.injured:
            choices = ['Scavenge for supplies',
                       'Fortify base',
                       'Hunt nearby ' + self.game.monsters,
                       'Keep watch',
                       'Get some rest']
            for i in range(len(choices)):
                print str(i) + '. ' + choices[i]
            choice = input('\nWhat should ' + self.name + ' do today? (Enter a number.)\n')
            self.perform_action(choices[choice])
        else:
            # Attempt to resolve injury
            recovery_chance = 33
            if self.game.base.medicine > 0:
                print self.name + ' took some medicine.'
                recovery_chance = 66

            if random.randint(0, 100) <= recovery_chance:
                print self.name + ' is looking better today. They can probably help again tomorrow.'
            else:
                print self.name + ' doesn\'t look much better today.'

    def perform_action(self, action):
        actions = {
            'Fortify base': {
                'success': 'NAME made some improvements to the base.',
                'failure': 'NAME didn\'t get much done around the base today.'
            },
            'Kill': {
                'success': 'NAME took out a horde of MONSTERS wandering close to the base.',
                'failure': 'NAME was injured while trying to kill MONSTERS around the base.',
                'big_failure': 'NAME went out to kill MONSTERS ... but they didn\'t come back.'
            },
            'Keep watch': {
                'success': 'NAME kept watch all day and took out a few MONSTERS.',
                'failure': 'NAME kept watch all day, but nothing came by.'
            },
            'Get some rest': {
                'success': 'NAME stayed in today and tried to relax.',
            }
        }

        action_roll = random.randint(0, 100)
        infection_roll = random.randint(0, 100)
        if self.rested:
            self.rested = False
            action_roll += 10

        if action == 'Scavenge for supplies':
            if action_roll > 75:
                self.game.base.supplies += random.randint(1, 3)
                self.game.base.medicine += random.randint(1, 2)
                result = self.name + ' brought back some medicine from the pharmacy.'
            elif action_roll > 50:
                self.game.base.supplies += random.randint(1, 3)
                result = self.name + ' brought back a random assortment of supplies from town.'
            elif action_roll > 25:
                result = self.name + ' couldn\'t find anything useful while scavenging.'
            else:
                self.injured = True
                if infection_roll < 20:
                    self.infected = True
                result = self.name + ' was injured while looking for supplies.'
        elif action == 'Fortify base':
            if action_roll > 50:
                self.game.base.defense += random.randint(1, 3)
                result = self.name + ' made some improvements to the base.'
            else:
                result = self.name + ' didn\'t get much done around the base today.'
        elif action == 'Keep watch':
            if action_roll > 50 and self.game.base.danger > 1:
                self.game.base.danger -= 1
                result = self.name + ' kept watch all day and took out a few ' + self.game.monsters + '.'
            else:
                result = self.name + ' kept watch all day, but nothing came by.'
        elif action == 'Get some rest':
            self.rested = True
            result = self.name + ' stayed in today and tried to relax.'
        else:
            if action_roll > 30:
                result = self.name + ' took out a group of ' + self.game.monsters + ' wandering close to the base.'
            elif action_roll > 15:
                self.injured = True
                if infection_roll < 20:
                    self.infected = True
                result = self.name + ' was injured while trying to kill ' + self.game.monsters + ' around the base.'
            else:
                self.alive = False
                result = self.name + ' went out to kill ' + self.game.monsters + ' ... but they didn\'t come back.'
        print result
        input('Press enter to continue...')

    # Returns a (mostly useless) string about how the character is doing
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
            message += self.name + ' is injured and can\'t do anything today.\n'
        if self.infected:
            if self.infected_days < 3:
                message += self.name + ' is looking unwell.\n'
            elif self.infected_days < 6:
                message += self.name + ' is looking badly ill.\n'
            else:
                message += self.name + ' looks close to turning.\n'
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
    def __init__(self, name, player_count):
        self.name = name
        self.population = player_count
        self.supplies = 30
        self.medicine = 0
        self.defense = 3
        self.danger = 1

    def status_report(self):
        print '\nThere are ' + str(self.population) + ' of us left.'
        print 'We have ' + str(self.supplies) + ' days of food and water.'
        print 'We have ' + str(self.medicine) + ' medicine in stock.'
        print 'Our defenses will hold for ' + str(self.defense / self.danger) + ' more nights.\n'


def main():
    Game(4).play()

main()
