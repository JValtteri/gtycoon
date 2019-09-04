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
    if len(player.products) < 3:
        while True:
            makeProduct()
            if len(player.products) == 3:
                break
            elif player.credits < 1:
                break 

    else:
        research()
    
    if player.refinememt < 0.15:
        researchNode()

