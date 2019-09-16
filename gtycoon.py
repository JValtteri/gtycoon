#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.08.2019
# GPU-tycoon

import calc
import UI
try:
    from msvcrt import getch
except: pass
from math import log, e, sqrt
from engine import GameStatus, Player, REFINE
import ai

"""Game engine and main program"""

# players=[]

# def newPlayer():
#     players.append(Player())

# def newAiPlayer():
#     players.append(Player("ASIx", True))

if __name__ == "__main__":

    UI.intro()
    #getch()

    input("Press ENTER")

    game = GameStatus(1, 1)
    players = game.players

    while True:

        for p in game.players:

            print("============================")
            print("Player:     ", p.name)
            print("year:       ", p.year)
            print("refinement: ", round(p.refinememt,2))
            print("============================")


            if p.ai == False:
                UI.showMarket(p, game)
                UI.gameScreen(p, game)
            else:
                ai.aiTurn(p, game)
            p.year += 1
            p.refinememt =  p.refinememt / REFINE

            p.income = 0                     # Income is reset for update

            for c in p.products:

                # UPDATE the dynamic parameters about each chip
                #
                c.update_refinement()
                c.update_cost()
                c.update_price_delta(game)
                c.update_yeald()
                c.update_income(game)
                game.update_ptp()

                if c.inproduction == True:
                    p.income += c.income     # Income is added together (FOR A PROJECTION!!! Don't use this for anything but cosmetic stuff!)

            print("Projected earnigs for", p.name, "this year:", round(p.income), "M")
            print("==================================================================")

            try:
                getch()
            except:
                input()

        game.update_ptp()

        for p in players:
            p.income = 0                     # Income is reset for update
            for c in p.products:
                c.update_income(game)
                if c.inproduction == True:
                    p.income += c.income     # Income is added together
            p.credits += p.income            # Yearly income is deposited

    # when game is run on command line
