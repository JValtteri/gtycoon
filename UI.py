#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.08.2019
# UI

import calc
import sys
import engine
# from gtycoon import game

# To make platform independent
try:
    from msvcrt import getch
except: pass


def intro():
    print("""
    
    You are the CEO of a rising star of semiconductors.

    Steer your company to greatness. Design a product line-up, optimize 
    and tune for profit.

    ...

    """)

def ask(question=""):
    question = question+"\t: "
    print("\n\n")
    i = input(question)
    print("\n")
    return i

def statusBar(player):
    print("""

        company:  %s    \t\t   year:     %i
        credits:  %i M   \t\t   products: %i
        science:  %i   \t\t\t   income:   %i M
        general:  %i    \t\t\t   node:     %s
        refinem:  %f

    ===========================================================
    """ % (player.name, player.year, player.credits, len(player.products), player.science, player.income, player.generalization, calc.NODE[player.node], player.refinememt) )

def gameScreen(player, game):
    while True:

        statusBar(player)

        print("""
        C = Chip Design  \t\t  B = Rebrand
        R = Research     \t\t  S = Price Drop

        M = Show the market

        [space] = Next Turn

        \t\t\t\t  Q = Quit game instantly


        """)
        try:
            ch = getch()
        except:
            ch = input (">>")

        if ch.upper() in ["R", b"R"]:
            research(player)

        elif ch.upper() in ["B", b"B"]:
            pass

        elif ch.upper() in ["C", b"C"]:
            design(player, game)

        elif ch.upper() in ["S", b"S"]:
            pass

        elif ch.upper() in ["M", b"M"]:
            showMarket(player, game)

        elif ch.upper() in [b" ", "", " "]:
            if game.num_products < 1:
                print("What sort of a company doesn't have any products!?")
            else:
                break

        elif  ch.upper() in ["Q", b"Q"]:
            sys.exit("quit")

        else:
            print("woops")

def research(player):
    while True:

        statusBar(player)

        print("""
        CHOOSE RESEARCH SUBJECT:

                                        Cost
        S = Specific Architecture       %i M
        G = General Compute             %i M

        N = Smaller process node        %i M

        [space] = Exit

        """ % (player.research_cost(), player.research_cost(), player.node_cost() ) )

        try:
            ch = getch()
        except:
            ch = input(">>")


        if ch.upper() in ["S", b"S"]:
            researched = player.research(0)

        elif ch.upper() in ["G", b"G"]:
            researched = player.research(1)

        elif ch.upper() in ["N", b"N"]:
            researched = player.research_node()

        elif ch.upper() in ["", b" ", " "]:
            break
        else:
            print("woops")

        try:
            if researched == True:
                print("Researched!")
            else:
                print("Not enough credits")
                
            try:
                getch()
            except:
                input ()
        except:
            pass

def showMarket(player, game):
    "Prints the market situation"
    print("""
    MARKET SITUATION""")

    if player.products == []:
        print("\n\tIt's a virgin market")

    print('\t Name \t Perf \t Cost \t Price \t Sales \t Size  \t\tNode')
    for p in game.players:
        for c in p.products:
            if c.inproduction == True:
                line = '\t ' + c.name + '\t ' + str(c.perf) + '\t ' + str(round(c.chipCost()))  + '\t ' + str(c.price) + ' c\t ' + str(round(c.sales(game))) + 'k \t ' + str(c.size) + ' mm2 \t' + str(calc.NODE[c.node]) 
                print(line)

def design(player, game):
    "Design a chip"

    ### PLEASE ####
    #
    # Find a sane way to split this in to sections.
    # This is horrible to read.

    statusBar(player)
    showMarket(player, game)
    print("\n\n\n\n")

    # Asks if there is a new chip designed, that is not in production
    try:
        no_saved = player.products[-1].inproduction
    except:
        # If there are no chips at all, there are no saved chips either
        no_saved = True

    # START FRESH
    # THE BASICS
    if no_saved:
        name = input("Chip name: ")
        size = int( input("Chip size: ") )
        price = 1
        overdrive = 0

        new_product = engine.Product(name, size, overdrive, price, player.node, player.science, player.refinememt)
        
        # The chip is added to products (saved), it will be refrenced to as 
        # player.products[-1] ig. Players newest product.
        player.products.append(new_product)

    # RECALL AN UNFINISHED CHIP
    else:
        # If a saved chip is found, the preliminary specs are displayed
        print("Chip name: ", player.products[-1].name)
        print("Chip size: ", player.products[-1].size)
        print("Overdrive: ", player.products[-1].overdrive)
        print("Chip price:", player.products[-1].price)
        print("\n")


    # MANUFACTURING
    #
    # Yeald and cost to make are tuned
    chipcost = player.products[-1].chipCost()

    print( "" )
    print( "Manufacturing cost per chip: \t", round( chipcost, 2), "c" )
    print( "Manufacturing yeald:         \t", round( player.products[-1].yealdPr()*100 ), "%" )


    # FINE TUNING THE PRODUCT
    while True:
        try:
            overdrive = float( input("Overdrive:\n\t\t\t\t-24 = 99%, \n\t\t\t\t-13 = 90%, \n\t\t\t\t -9 = 80%, \n\t\t\t\t  0 = nominal (50%), \n\t\t\t\t  9 = top 20%, \n\t\t\t\t 13 = top 10%\n\n> ") )
        except ValueError:
            overdrive = 0
        player.products[-1].overdrive = overdrive
        chipcost = player.products[-1].chipCost()
        print( "" )
        print( "Manufacturing cost per chip: \t", round( chipcost, 2), "c" )
        print( "Manufacturing yeald:         \t", round( player.products[-1].yealdPr()*100 ), "%" )
        print( "Total yeald:                 \t", round( player.products[-1].yealdPr() * player.products[-1].skewYeald() *100 ), "%" )

        print("\nProceed? Y/n")
        try:
            ch = getch()
        except:
            ch = input(">>")
        if ch.upper() in ['N', b'N']:
            pass
        elif ch.upper() in ['', 'Y', ' ', b'\r', b'Y', b' ']:
            break
        else:
            pass


    # PRICE SELECTION
    #
    # Proposes a price for the player
    # pprice = round(chipcost*1.1)
    print("\nChoose chip price:")
    print("Press enter for default (10%%) margin price: (%i c) \nor enter a price. (Minimum ~26)" % round(chipcost*1.1) )
    try:
        price = int( input("> ") )
    except:
        print("Using default price")
        price = round(chipcost * 1.1)
    if price < 26:
            price = 26
            print("""
            Price set too low!
            It won't cover the packaging costs.
            But don't worry. I raised the price abit. It should be fine now.
            New price is %i c
            """ % price)
    try:
        getch()
    except:
        input()
    player.products[-1].price = price

    # Is the maximum number of chips reached?
    if len(player.products) >= engine.MAX_CHIPS:
        print("""
        Maximum number of chips reached.
        The oldest chip will be removed:
        """)
        print(player.products[0].name, player.products[0].node, player.products[0].size, "mm2", player.products[0].price, "c")


    # PRODUCTION AND TRANSACTION
    statusBar(player)
    print("""
    It costs %i M to start production.
    Do you whant to procede with producing this chip? (y/N)
    """ % engine.PRODUCTION_COST)
    try:
        ch = getch()
    except:
        ch = ch = input("")

    if ch.upper() in ['Y', b'Y']:
        done = player.purchase(engine.PRODUCTION_COST)

        if done == True:

            player.products[-1].inproduction = True
            market_segment = player.products[-1].market()
            game.newProduct(market_segment, price, player.products[-1].performance())
            # player.income += player.products[-1].get_income(game)				# PROBLEMATIC!!! GET INCOME ASKS FOR GAME PTP THAT IS NONE

            # game.ref_market += player.products[-1].market()
            # game.num_products += 1

            print("Transaction complete\nChip Released")
        else:
            print("Not enough credits!")
        try:
            getch()
        except:
            input()

    elif ch.upper() in ['N', b'N']:
        print("""
        Do you whant to save the chip for later?
        (Y/n)
        """)
        try:
            getch()
        except:
            ch = input(">>")
        if ch.upper() in ['N', b'N']:
            del player.products[-1]
            print("Deleted")
        else:
            pass


