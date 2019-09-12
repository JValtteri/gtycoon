#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.08.2019
# GPU-tycoon

import calc
import UI
# from msvcrt import getch
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

        game.update_ptp()

        for p in game.players:

            if p.ai == False:
                UI.showMarket(p, game)
                UI.gameScreen(p, game)
            else:
                ai.aiTurn(p, game)
            p.year += 1
            p.refinememt =  p.refinememt / REFINE

            p.income = 0    # Income is reset for update

            for c in p.products:

                # Update the dynamic parameters about each chip
                c.update_refinement()
                c.update_cost()
                c.update_price_delta(game)
                c.update_yeald()
                c.update_income(game)

                if c.inproduction == True:
                    p.income += c.income    # Income is added together

            # Yearly income is deposited
            p.credits += p.income

            print("\n", p.name, "This years earnings:", p.income, "c")

            try:
                getch()
            except:
                input()

    print(("year:", players[0].year))
    print(("year:", players[0].refinememt))

    # when game is run on command line

