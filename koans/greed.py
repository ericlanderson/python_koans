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

#############################################
# Class Player
#############################################
class Game:
    def __init__(self,names,min_score,max_score):
        self._players = []
        self.round = 1
        self.over = False
        self._message = ""
        self.final_round = False
        self.leader = Player()
        self.min_score = min_score
        self.max_score = max_score
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

    def play(self):
        while not self.over: 

            if self.leader.score >= self.max_score:
                self.final_round = True
                self.remove_player(self.leader)
                self.message = "(final round)"

            print("******************************************************")
            print("Round:",self.round,self.message)

            for player in self.players:
                
                self.take_turn(player)        
                            
            self.next_round()

        self.end()

    def take_turn(self,player):

        player.scratched = False
        turn_over = False
        turn_score = 0
        remaining_dice = 5
        message = "."

        print(player.name,"is taking their turn and currently has",player.score,"points.")

        while not turn_over:
            dice = DiceSet()
            dice.roll(remaining_dice)
            print(player.name,"rolled",dice.values,"which is",dice.score,"points.")
            if dice.score > 0:
                turn_score += dice.score
                # Final turn
                if self.final_round:
                    if player.score + turn_score > self.leader.score:
                        turn_over = True
                # Regular turn
                elif player.score > self.min_score:
                    if dice.remaining == 1:
                        turn_over = True
                # Not on the board
                else:
                    if turn_score >= self.min_score:
                        turn_over = True
                        print(player.name,"got on the board with", turn_score,"points")

                if dice.remaining == 0:
                    remaining_dice = 5
                else:
                    remaining_dice = dice.remaining
            else:
                player.scratched=True
                turn_over = True

        if player.scratched:
            print(player.name,"scratched and lost",turn_score,"points.")
        else:
            player.score += turn_score

            if player.score > self.leader.score:
                self.leader = player
                message = "and is now the leader."

            print(player.name,"ends with",remaining_dice,"dice remaining and scored",turn_score,"points.")
            print(player.name,"now has", player.score,"points",message)

    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self,msg):
        self._message = msg

###########################################################
# Class Player
###########################################################
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
###########################################################
# Class DiceSet
###########################################################
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

###########################################################
# Main ...
###########################################################
min_score = 300
max_score = 3000

# Our list of players
players = ["Andy","Candy","Mandy","Sandy","Glenn Dandy"]

# Create our game with the players
game = Game(players, min_score, max_score)

# play the game
game.play()