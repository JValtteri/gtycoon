#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 25.08.2019
# AI

import calc
import engine

# class Ai():

#     def __init__(self, name = "xVidia"):
#         self.name = name

def aiTurn(player, ai_type = 0):
    print("Ai Turn")
    if ai_type == 0:
        typeAturn(player)


def typeAturn(player):   
    if len(player.products) >= 3:    # If a full product stack exists...
        player.research()            # Research architecture
        if player.refinememt < 0.15:
            player.research(2)    # Research NODE
        #if player.products[-3].node == player.node: # If the last 3 chips are current node, buy a new node if possible
        #    doNode(player)
    makeAproduct(player)
    research(player)

 
def makeAproduct(player):
    # Try transaction, if true go on...
    if player.purchase(engine.PRODUCTION_COST):
        if len(player.products) % 3 == 0: # make Low end / make first product
            name = "A10"
            size = 40
            overdrive = -8
            price = 50
        elif len(player.products) % 3 == 1: # make mid range
            name = "A20"
            size = 150
            overdrive = -5
            price = 190
        elif len(player.products) % 3 == 2: # make High end
            name = "A30"
            size = 240
            overdrive = 3
            price = 50
        print(name, "released")
        new_product = engine.Product(name, size, overdrive, price, player.node, player.science, player.refinememt)
        chipcost = new_product.chipCost()
        new_product.price = round(chipcost * 1.1)
        player.products.append(new_product)
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



