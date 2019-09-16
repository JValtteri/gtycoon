#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 25.08.2019
# AI

import calc
import UI
import engine
try:
    from msvcrt import getch
except:
    pass

# class Ai():

#     def __init__(self, name = "xVidia"):
#         self.name = name

def aiTurn(player, game, ai_type = 0):
    print("\n\n\n==================\nAi Turn\n==================\n\n\n")
    try: getch()
    except: input()

    if ai_type == 0:
        typeAturn(player, game)


def typeAturn(player, game):
    if len(player.products) <= engine.MAX_CHIPS:
        doResearch(player)
        makeAproduct(player, game)

    elif player.refinememt < 0.15:                        # If the node is old
        priceCut(player, game, 1)
        doResearch(player)

    elif len(player.products) < 0.2:  #engine.MAX_CHIPS:        # If a full product stack exists...
        if player.products[-1].node != player.node:
            doResearch(player, 0)
            makeAproduct(player, game)
        else:
            doResearch(player, 1)
            makeAproduct(player, game)

def doResearch(player, mode=0):
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
            else: print("%s Researched a %s node" % (player.name, calc.NODE[player.node] ))
    if mode in [0, 2]:
        while True:                          # Research other stuff 'till out of money
            money_to_spend = player.research(0)
            if money_to_spend != True:
                break
            else: print("Ai did research")


def priceCut(player, game):
    for product in player.products:
        game.remove_from_market(product)    # Remove the old product from market
        chipcost = product.chipCost()       # Count chipcost to guide pricing
        price = round(chipcost * 1.08)
        player.product.price = price
        game.newProduct(product)            # Add the pricecut product back to market
        UI.productReleace(player, product, game, "PRICEDROP")


def makeAproduct(player, game):
    # Try transaction, if true go on...
    if player.purchase(engine.PRODUCTION_COST):
        if len(player.products) == 4:
            if player.products[0].name[-2] == "4":
                name = "A40"
                size = 450
                overdrive = -12
            elif player.products[0].name[-2] == "3":
                name = "A30"
                size = 350
                overdrive = -11
            elif player.products[0].name[-2] == "2":
                name = "A20"
                size = 250
                overdrive = -12
            elif player.products[0].name[-2] == "1":
                name = "A10"
                size = 110
                overdrive = -14
            else:
                print("Error: 4 products, Could not recognize the chip")

        else: # make Low end / make first product
            if len(player.products) == 0: # make low end
                name = "A10"
                size = 105
                overdrive = -14
            elif len(player.products) == 1: # make mid range
                name = "A20"
                size = 250
                overdrive = -12
            elif len(player.products)  == 2: # make High end
                name = "A30"
                size = 320
                overdrive = -11
            elif len(player.products)  == 3: # make High end
                name = "A40"
                size = 365
                overdrive = -11

        if len(player.products) >= 4:               # If a full product stack exits
            old_product = player.products[0]        # Oldest card is replaced
            game.remove_from_market(old_product)    # old_product.market(), old_product.price, old_product.pref)

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
        try: getch()
        except: input()

        game.newProduct(player.products[-1])            # market_segment, price, player.products[-1].performance())
        player.income += player.products[-1].get_income(game)
