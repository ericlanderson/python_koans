#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

import random

class Game:
    def __init__(self,names):
        self._players = []
        self._message = ""
        for name in names:
            print("Adding ",name, " to the game.")
            self._players.append(Player(name))

    @property
    def players(self):
        return self._players

    @property
    def leader(self):
        leader = ""
        highest_score = 0
        for player in self._players:
            if player.score > highest_score:
                leader = player.name
                highest_score = player.score
        return Player(leader, highest_score)

    def remove_player(self,leader):
        for player in self._players:
            if player.name == leader.name:
                self._players.remove(player)

    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self,msg):
        self._message = msg

class Player:
    def __init__(self,name, score = 0):
        self._name = name
        self._score = score
 
    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

class DiceSet:
    def __init__(self):
        self._values = None
        self._score = 0
        self._remaining = 0

    @property
    def values(self):
        return self._values

    @property
    def score(self):
        return self._score

    @property
    def remaining(self):
        return self._remaining

    def roll(self, n):
        self._values = []
        for die in range(n):
            self._values.append(random.randint(1,6))
        self.dice_score()

    def dice_score(self):
        score = 0
        remaining = 0
        # Dictionary for the dice results we care about
        die_result_score = {1:100, 5:50}

        # Prepare a dictionary of the possible dice roll results
        die_result_count = {}.fromkeys(range(1,7),0)

        # Count the results for each die
        for die in self._values:
            die_result_count[die] += 1

        # Process each die to compute the score        
        for die in self._values:
            if die_result_count[die] >= 3:
                if die == 1:
                    score += 1000
                else:
                    score += 100 * die
                die_result_count[die] -= 3
            
            if die == 1 or die == 5:
                score += die_result_score[die] * die_result_count[die]
                die_result_count[die] = 0

        # Count the remaining dice which did not score if the score > 0
        if score > 0:
            for die in die_result_count:
                if die_result_count[die] > 0:
                    remaining += die_result_count[die]
        
        # print("DEBUG: score:", score, "remaining: ",remaining)

        self._score = score
        self._remaining = remaining

max_score = 3000

players = ["Andy","Candy","Mandy","Sandy","Glenn Dandy"]
game = Game(players)

leader = Player("Anon",0)

game.rounds = 0
game.over = False
final_round = False
while not game.over: 

    game.rounds += 1

    if leader.score >= max_score:
        final_round = True
        game.remove_player(leader)
        game.message = "(final round)"

    print("******************************************************")
    print("Round:",game.rounds,game.message)

    for player in game.players:
        print(player.name, "is taking a turn and currently has",player.score,"points.")
        
        remaining_dice = 5
        turn_score = 0
        scratched = False
        turn_is_over = False

        # If this is the final round, play until you beat the leader or scratch ...            
        if final_round:
            print(player.name,"is taking their final turn.")
            while not turn_is_over and not scratched:
                if player.score + turn_score < leader.score and remaining_dice > 0:
                    dice = DiceSet()
                    dice.roll(remaining_dice)
                    print(player.name,"rolled",dice.values)
                    if dice.score > 0:
                        turn_score += dice.score
                        remaining_dice = dice.remaining
                    else:
                        scratched=True
                        print(player.name,"scratched and will score 0 points.")
                else:
                    turn_is_over = True
                    player.score += turn_score
                    print(player.name,"ends with",remaining_dice,"dice remaining and scored",turn_score,"points.")
                    print(player.name,"now has", player.score,"points.")
            
        # Does this player still need to get on the board?
        elif player.score < 300:
            print(player.name,"is trying to get on the board.")
            
            while remaining_dice > 0 and turn_score < 300:
                dice = DiceSet()
                dice.roll(remaining_dice)
                print(player.name,"rolled", dice.values)
                turn_score += dice.score
                remaining_dice = dice.remaining
                
            if turn_score >= 300:
                player.score = turn_score
                print(player.name,"got on the board with", player.score,"points")
            else:
                print(player.name,"failed to get on the board with", turn_score,"points")

        else:
            while not turn_is_over and not scratched:
                if remaining_dice >=3:
                    dice = DiceSet()
                    dice.roll(remaining_dice)
                    print(player.name,"rolled",dice.values)
                    if dice.score > 0:
                        turn_score += dice.score
                        remaining_dice = dice.remaining
                    else:
                        scratched=True
                        print(player.name,"scratched and will score 0 points.")
                else:
                    turn_is_over = True
                    player.score += turn_score
                    print(player.name,"will stop with",remaining_dice,"dice remaining and scored",turn_score,"points.")
                    print(player.name,"now has", player.score,"points.")
                    
    if final_round: 
        game.over = True
        final_round_leader = game.leader
        if final_round_leader.score > leader.score:
            leader = final_round_leader
    else:
        leader = game.leader
        print("End of round",game.rounds,":",leader.name,"is now the leader with",leader.score,"points.")

print("******************************************************")
print("After",game.rounds,"rounds,",leader.name,"is the winner with",leader.score,"points.")
            
        
