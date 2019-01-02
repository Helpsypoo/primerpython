import math
import statistics
import random

class Player(object):
    def __init__(
        self,
        first_num_passes = 0,
        second_num_passes = 0
    ):
        self.score = 0
        self.first_num_passes = first_num_passes
        self.second_num_passes = second_num_passes


class Tournament(object):
    def __init__(
        self,
        max_game_length = 10,
        initial_players = None,
        num_player_target = 1000,
        mutation_chance = 0
    ):
        self.max_game_length = max_game_length
        self.mutation_chance = mutation_chance

        #Default initial player set is one of each possible strategy
        if initial_players == None or initial_players == 'spread':


            num_kinds = round(math.sqrt(num_player_target))
            spacing = self.max_game_length / (num_kinds - 1)
            initial_players = []
            for i in range(num_kinds):
                for j in range(num_kinds):
                    player = Player(
                        first_num_passes = round(i * spacing),
                        second_num_passes = round(j * spacing)
                    )
                    initial_players.append(player)

        elif initial_players == 'trusters':
            initial_players = []
            for i in range(num_player_target):
                player = Player(
                    first_num_passes = self.max_game_length,
                    second_num_passes = self.max_game_length
                )
                initial_players.append(player)
        elif initial_players == 'untrusters':
            initial_players = []
            for i in range(num_player_target):
                player = Player(
                    first_num_passes = 0,
                    second_num_passes = 0
                )
                initial_players.append(player)

        if not isinstance(initial_players, list):
            raise Warning('Initial player set must be a list')

        #Ensure num_player_target is set. Sometimes redundant.
        self.num_player_target = len(initial_players)
        print(self.num_player_target)

        self.round_log = [initial_players]


    def play_round(self):
        print('Playing round ' + str(len(self.round_log)))
        #Play games
        players = self.round_log[-1]
        #print(len(players))
        #Let each pair of players play twice, swapping first move
        for player in players:
            for other_player in players:
                if player != other_player:
                    self.play_game(player, other_player)

        #Create next player set
        tot_score = sum([x.score for x in players])
        #print(tot_score)

        next_players = []

        #For each possible strategy, award offspring number proportional to
        #total score of that strategy
        #Doesn't take care of mutations below zero or above the max.
        #Just kills them. Eh.
        for i in range(self.max_game_length + 1):
            for j in range(self.max_game_length + 1):
                pws = [x for x in players if \
                        x.first_num_passes == i and x.second_num_passes == j]

                s_score = sum([x.score for x in pws])
                num_offspring = round(s_score / tot_score * self.num_player_target)


                for k in range(num_offspring):
                    f_var = 0
                    s_var = 0
                    mutation_roll = random.random()
                    if mutation_roll < self.mutation_chance / 4:
                        f_var = 1
                    elif mutation_roll < self.mutation_chance / 2:
                        f_var = -1
                    elif mutation_roll < 3 * self.mutation_chance / 4:
                        s_var = 1
                    elif mutation_roll < self.mutation_chance:
                        s_var = -1

                    new_player = Player(
                        first_num_passes = i + f_var,
                        second_num_passes = j + s_var
                    )
                    next_players.append(new_player)

        #print(len(next_players))

        self.round_log.append(next_players)

    def play_game(self, player1, player2):
        if player1.first_num_passes >= self.max_game_length / 2 and \
           player2.second_num_passes >= self.max_game_length / 2:
            player1.score += 2 * self.max_game_length
            player2.score += 2 * self.max_game_length
        elif player1.first_num_passes <= player2.second_num_passes:
            player1.score += 2 + 2 * player1.first_num_passes
            player2.score += 2 * player1.first_num_passes
        elif player1.first_num_passes > player2.second_num_passes:
            player1.score += 1 + 2 * player2.second_num_passes
            player2.score += 3 + 2 * player2.second_num_passes

    def print_stats(self):
        print()
        for rou in self.round_log:
            fnps = [x.first_num_passes for x in rou]
            avg_fnp = statistics.mean(fnps)
            std_dev_fnp = statistics.pstdev(fnps)

            snps = [x.second_num_passes for x in rou]
            avg_snp = statistics.mean(snps)
            std_dev_snp = statistics.pstdev(snps)

            print(
                str(round(avg_fnp, 1)) + ', ' + \
                str(round(std_dev_fnp, 1)) + ', ' + \
                str(round(avg_snp, 1)) + ', ' + \
                str(round(std_dev_snp, 1)) + ', ' + \
                str(len(rou))
            )
            #print()
