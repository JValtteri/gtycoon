#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 25.08.2019
# AI

import calc
import UI
import engine

import random
import time
try:
    from msvcrt import getch
except:
    pass

# class Ai():

#     def __init__(self, name = "xVidia"):
#         self.name = name

def aiTurn(player, game, ai_type = 1):
    print("\n\n\n==================\nAi Turn\n==================\n\n\n")
    #try: getch()
    #except: input()
    time.sleep(2)

    if ai_type == 0:
        typeAturn(player, game)
    elif ai_type == 1:
        typeBturn(player, game)


def typeAturn(player, game):
    if len(player.products) < engine.MAX_CHIPS:
        doResearch(player, 0)
        makeAproduct(player, game)

    elif player.refinememt < 0.2:                        # If the node is old
        priceCut(player, game, 1)
        doResearch(player, 1)

    elif len(player.products) >=  engine.MAX_CHIPS:        # If a full product stack exists...
        if player.products[-1].node != player.node:
            doResearch(player, 0)
            makeAproduct(player, game)
        else:
            doResearch(player, 1)
            makeAproduct(player, game)


def typeBturn(player,game):
    if len(player.products) < 1:
        makeBproduct(player, game, 1)
    if len(player.products) < engine.MAX_CHIPS:
        makeBproduct(player, game, 2)
        makeBproduct(player, game, 3)
        makeBproduct(player, game, 4)
        doResearch(player, 1)

    elif player.refinememt == 0.4:
        makeBproduct(player, game, 2)
        makeBproduct(player, game, 3)
        makeBproduct(player, game, 4)

    elif player.refinememt > 0.3:
        if game.best_ptp / player.products[-1].ptp < 0.8:
            priceCut(player, game)
            doResearch(player, 1)
        makeBproduct(player, game, 5)
        doResearch(player, 0)

    elif player.refinememt > 0.23:
        priceCut(player, game)
        makeBproduct(player, game, 6)
        doResearch(player, 1)

    elif player.refinememt < 0.23:
        priceCut(player, game)

        # Calculate, which is better, to research node or architecture
        #
        if player.research_cost() * 1.82 < player.node_cost():
            for i in range(10):
                doResearch(player, 2)
        else:
            doResearch(player, 1)

        # If the research worked, a new line of products can be releaced
        #
        if player.products[-1].node != player.node or player.products[-1].science != player.science:
            makeBproduct(player, game, 2)
            makeBproduct(player, game, 3)
            makeBproduct(player, game, 4)
            makeBproduct(player, game, 5)

        # If the last chip made is not a X60 chip, make one now.
        #
        elif player.products[-1].name[-2] != 6:
            makeBproduct(player, game, 6)

        # If all else fails, cut prices and hope for the best
        # Ehem... prices were cut before this step already



def doResearch(player, mode):
    """
    Mode 0 = research all
    Mode 1 = research Node
    Mode 2 = research Architecture
    """
    if mode in [0, 1]:
        while True:                          # Research nodes 'till out of money
            money_to_spend = player.research_node()
            if money_to_spend != True:
                break
            else:
                print("%s Researched a %s node" % (player.name, calc.NODE[player.node] ))
                time.sleep(1)

    if mode in [0, 2]:
        # while True:                          # Research other stuff 'till out of money
        money_to_spend = player.research(0)
            # if money_to_spend != True:
            #     break
            # else: print("Ai did research")


def priceCut(player, game):
    for product in player.products:
        game.remove_from_market(product)    # Remove the old product from market
        chipcost = product.chipCost()       # Count chipcost to guide pricing
        price = round(chipcost * 1.08)
        product.price = price
        game.newProduct(product)            # Add the pricecut product back to market
        UI.productReleace(player, product, game, "PRICEDROP")


def makeBproduct(player, game, type):
    # Try transaction, if true go on...
    if player.purchase(engine.PRODUCTION_COST):
        # Define the product brand name
        if len( player.products ) == 0:
            brands = ["A", "K", "S", "T", "G", "X", "Z", "C", "M", "R", "e", "E"] #'SX', 'CX', 'MX', 'RS'
            brand = random.choice(brands)
        else:
            brand = player.products[0].name[0]

        if type == 1:
            name = brand + "10"
            size = random.choice([90, 100, 110, 120])
            overdrive = random.choice([-12, -11, -10])
            margin = 1.2

        elif type == 2:
            name = brand + "20"
            size = random.choice([240, 250, 260])
            overdrive = random.choice([-12, -11, -10, -9])
            margin = 1.1

        elif type == 3:
            name = brand + "30"
            size = random.choice([330, 340, 350, 360])
            overdrive = random.choice([-12, -11, -10, -9])
            margin = 1.1

        elif type == 4:
            name = brand + "40"
            size = random.choice([430, 440, 450, 460])
            overdrive = random.choice([-12, -11, -10, -9])
            margin = 1.2

        elif type == 5:
            name = brand + "50"
            size = random.choice([530, 540, 550, 560])
            overdrive = random.choice([-14, -13, -12, -11, -10, -9])
            margin = 2.5

        elif type == 6:
            name = brand + "60"
            size = random.choice([650, 655, 660, 665])
            overdrive = random.choice([-10, -9, -8, -7, -6])
            margin = 2.3

        else:
            print("ERROR: CHIP TYPE OUT OF RANGE!")

        if len(player.products) >= engine.MAX_CHIPS: # If a full product stack exits
            old_product = player.products[0]         # Oldest card is replaced
            game.remove_from_market(old_product)     # old_product.market(), old_product.price, old_product.pref)

            # For example: Replace A20 with A120
            if len( player.products[-1].name ) == 3:
                name = name.replace(brand, brand + '1')

            else:
                if player.node == player.products[-1].node and player.science == player.products[-1].science:
                    series = str(player.products[-1].name[1])              # series number
                else:
                    series = str( int( player.products[-1].name[1] ) + 1 ) # Iterate series number
                name = brand + series + name.strip(brand)                  # New name is derived

            del[player.products[0]]

        new_product = engine.Product(name, size, overdrive, 1, player.node, player.science, player.refinememt)
        chipcost = new_product.chipCost()           # Count chipcost to guide pricing
        price = round(chipcost * margin)            # Sets the price by chip cost
        if price < 26:                              # If the price is too low
            price = 26                              # set the minimum price.
        new_product.price = price                   # Save it in the product
        player.products.append(new_product)
        player.products[-1].inproduction = True
        UI.productReleace(player, player.products[-1], game)
        #try: getch()
        #except: input()
        time.sleep(2)

        game.newProduct(player.products[-1])
        player.income += player.products[-1].get_income(game)


def makeAproduct(player, game):
    # Try transaction, if true go on...
    if player.purchase(engine.PRODUCTION_COST):
        if len(player.products) == 4:
            if player.products[0].name[-2] == "5":
                name = "A50"
                size = 540
                overdrive = -13
            elif player.products[0].name[-2] == "4":
                name = "A40"
                size = 450
                overdrive = -11
            elif player.products[0].name[-2] == "3":
                name = "A30"
                size = 350
                overdrive = -11
            elif player.products[0].name[-2] in ["1", "2"]:
                name = "A20"
                size = 250
                overdrive = -12
            elif player.products[0].name[-2] == "1":
                name = "A10"
                size = 110
                overdrive = -12
            #else:
            #    print("Error: 4 products, Could not recognize the chip")

        else: # make Low end / make first product
            if len(player.products) == 0: # make low end
                name = "A10"
                size = 105
                overdrive = -8
            elif len(player.products) == 1: # make mid range
                name = "A20"
                size = 250
                overdrive = -10
            elif len(player.products)  == 2: # make High end
                name = "A30"
                size = 320
                overdrive = -12
            elif len(player.products)  == 3: # make High end
                name = "A40"
                size = 365
                overdrive = -14

        if len(player.products) >= engine.MAX_CHIPS: # If a full product stack exits
            old_product = player.products[0]         # Oldest card is replaced
            game.remove_from_market(old_product)     # old_product.market(), old_product.price, old_product.pref)

            bace_name = player.products[0].name
            if bace_name == name:
                name = name.replace('A', 'A1')
            else:
                old_name = bace_name.strip('A')
                series = str(int(old_name[0]) + 1)      # Iterate series number
                name = "A" + series + name.strip('A')   # New name is derived

            #player.products[len(player.products)%3].inproduction = False
            del[player.products[0]]

        new_product = engine.Product(name, size, overdrive, 1, player.node, player.science, player.refinememt)
        chipcost = new_product.chipCost()           # Count chipcost to guide pricing

        price = round(chipcost * 1.1)               # Sets the price by chip cost
        if price < 26:                              # If the price is too low
            price = 26                              # set the minimum price.
        new_product.price = price                   # Save it in the product

        player.products.append(new_product)
        player.products[-1].inproduction = True
        # market_segment = player.products[-1].market()

        UI.productReleace(player, player.products[-1], game)
        #try: getch()
        #except: input()
        time.sleep(2)

        game.newProduct(player.products[-1])            # market_segment, price, player.products[-1].performance())
        player.income += player.products[-1].get_income(game)
