#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 25.08.2019
# AI

import calc
import engine

# class Ai():

#     def __init__(self, name = "xVidia"):
#         self.name = name

def aiTurn(player, game, ai_type = 0):
    print("\n\n\n==================\nAi Turn\n==================\n\n\n")
    if ai_type == 0:
        typeAturn(player, game)


def typeAturn(player, game):   
    if len(player.products) >= 3:    # If a full product stack exists...
        player.research()            # Research architecture
        if player.refinememt < 0.15:
            player.research(2)    # Research NODE
        #if player.products[-3].node == player.node: # If the last 3 chips are current node, buy a new node if possible
        #    doNode(player)
    makeAproduct(player, game)
    player.research(player)


def makeAproduct(player, game):
    # Try transaction, if true go on...
    if player.purchase(engine.PRODUCTION_COST):
        if len(player.products) % 3 == 0: # make Low end / make first product
            name = "A10"
            size = 48
            overdrive = -8
            price = 50
        elif len(player.products) % 3 == 1: # make mid range
            name = "A20"
            size = 156
            overdrive = -5
            price = 190
        elif len(player.products) % 3 == 2: # make High end
            name = "A30"
            size = 248
            overdrive = 3
            price = 50
        print(name, "released")

        new_product = engine.Product(name, size, overdrive, price, player.node, player.science, player.refinememt)
        chipcost = new_product.chipCost()           # Count chipcost to guide pricing
        price = round(chipcost * 1.1)               # Sets the price by chip cost
        if price < 26:                              # If the price is too low
            price = 26                              # set the minimum price.
        new_product.price = price                   # Save it in the product
        player.products.append(new_product)
        player.products[-1].inproduction = True
        market_segment = player.products[-1].market()
        game.newProduct(market_segment, price)
        player.income += player.products[-1].get_income(game)







# SOME ALTERNATIVE LOGIC
#
#
#def spawnProduct(player):
    #
 #   new_product = engine.Product(name, size, overdrive, price, player.node, player.science, player.refinememt)
    # The chip is added to products (saved), it will be refrenced to as 
    # player.products[-1] eg. Players newest product.
  #  player.products.append(new_product)

#    if len(player.products) < 3:
#        while True:
#            makeProduct()
#            if len(player.products) == 3:
#                break
#            elif player.credits < 1:
#                break 



