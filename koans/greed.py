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
        self.round = 1
        self.over = False
        self._message = ""
        self.final_round = False
        self.leader = Player()
        for name in names:
            print("Adding ",name, " to the game.")
            self._players.append(Player(name))

    @property
    def players(self):
        return self._players
    
    def get_leader(self):
        current_leader = Player()
        highest_score = 0
        for player in self._players:
            if player.score > highest_score:
                current_leader = player
                highest_score = current_leader.score
        return current_leader

    def remove_player(self,leader):
        for player in self._players:
            if player.name == leader.name:
                self._players.remove(player)

    def next_round(self):
        if self.final_round: 
            # Game over
            self.over = True
            final_round_leader = self.get_leader()
            if final_round_leader.score > self.leader.score:
                self.leader = final_round_leader
        else:
            # End of current round
            self.leader = self.get_leader()
            if self.leader.name == "None":
                print("End of round",self.round,": There is no leader.")
            else:
                print("End of round",self.round,":",self.leader.name,"is the leader with",self.leader.score,"points.")

            self.round += 1

    def end(self):
        print("******************************************************")
        print("After",self.round,"rounds,",self.leader.name,"is the winner with",self.leader.score,"points.")

    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self,msg):
        self._message = msg

class Player:
    def __init__(self,name = "None", score = 0):
        self._name = name
        self._score = score
        self._message = ""
        self._scratched = False
 
    @property
    def name(self):
        return self._name

    @property 
    def score(self):
        return self._score

    @property
    def scratched(self):
        return self._scratched

    @scratched.setter
    def scratched(self, value):
        self._scratched = value

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self,msg):
        self._message = msg

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

def take_turn(player,remaining_dice,turn_score):
    dice = DiceSet()
    dice.roll(remaining_dice)
    print(player.name,"rolled",dice.values,"which is",dice.score,"points.")
    if dice.score > 0:
        turn_score += dice.score
        if dice.remaining > 0:
            remaining_dice = dice.remaining
        else:
            remaining_dice = 5
    else:
        player.scratched=True
    
    return player, remaining_dice, turn_score

max_score = 3000

players = ["Andy","Candy","Mandy","Sandy","Glenn Dandy"]
game = Game(players)

while not game.over: 

    if game.leader.score >= max_score:
        game.final_round = True
        game.remove_player(game.leader)
        game.message = "(final round)"

    print("******************************************************")
    print("Round:",game.round,game.message)

    for player in game.players:
        
        remaining_dice = 5
        turn_score = 0
        scratched = False
        player.scratched = False
        turn_is_over = False

        # If this is the final round, play until you beat the leader or scratch ...            
        if game.final_round:
            print(player.name,"is taking their final turn and currently has",player.score,"points.")
            while player.score + turn_score < game.leader.score \
                  and remaining_dice > 0 \
                  and not player.scratched:
                player, remaining_dice, turn_score = take_turn(player,remaining_dice,turn_score)
             
            if not player.scratched:
                player.score += turn_score
                print(player.name,"ends with",remaining_dice,"dice remaining and scored",turn_score,"points.")
                print(player.name,"now has", player.score,"points.")
                if player.score > game.leader.score:
                    game.leader = player
                    print(game.leader.name,"is the new leader.")

            else:
                print(player.name,"scratched and lost",turn_score,"points.")

        # Does this player still need to get on the board?
        elif player.score < 300:
            print(player.name,"is trying to get on the board.")
            
            # keep rolling until we have > 300 
            while remaining_dice > 0 and turn_score < 300 and not player.scratched:
                player, remaining_dice, turn_score = take_turn(player,remaining_dice,turn_score)
                   
            if turn_score >= 300:
                player.score = turn_score
                print(player.name,"got on the board with", player.score,"points")
            else:
                print(player.name,"failed to get on the board with", turn_score,"points")

        else:
            print(player.name, "is taking a turn and currently has",player.score,"points.")

            # Regular turn but stop when one die remains.
            while remaining_dice > 1 and not player.scratched:
                player, remaining_dice, turn_score = take_turn(player,remaining_dice,turn_score)
             
            if not player.scratched:
                player.score += turn_score
                print(player.name,"will stop with",remaining_dice,"dice remaining and scored",turn_score,"points.")
                print(player.name,"now has", player.score,"points.")
            else:
                print(player.name,"scratched and will score 0 points.")
                    
    game.next_round()

game.end()