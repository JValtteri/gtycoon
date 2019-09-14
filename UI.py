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

def productReleace(player, product, game, rebrand=False):
    "Announcement of a new product and a brief review"
    #product = player.products[-1]
    review_word = "in mid range."
    review = product.name + " is a new, compelling offering from a compelling offering \n" + player.name + " deliivers on their promice to deliver more performance in its segment."

    if product.price > 300:
        review_word = "in the hign-end market."

    elif product.price < 100:
        review_word = "\nAnd it is an interesting offering in the budjet segment."

    if rebrand == True:
        review_word = "rebrand" + review_word

    # MAXIMUM PERFORMANCE
    perf_max = game.max_perf
    #for p in game.players:
    #    for c in p.products:
    #        if c.perf >= perf_max:
    #            perf_max = c.perf

    if product.perf == perf_max:
        review = "The new product sets the standard for technology to come."
        if product.ptp == game.best_ptp:
            review_word = "to universal acclaim."
    elif product.ptp == game.best_ptp:
        review = product.name + "is the best thing since sliced bread. It is the best value out there."
    elif product.ptp < game.best_ptp*1.1 :
        review = product.name + " offers great value that is hard to beat in the current market."
    elif product.ptp >= game.avg_ptp:
        review = product.name + " francly, is an example of the never ending greed of modern companies \nripping off their customers."


    # PACKAGE THE ANNOUNCEMENT
    print("========================= TECH POINT ==========================\n")
    print(player.name, "releaced", product.name,  review_word, "\n")
    print(review)
    print("===============================================================")


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
        C = Chip Design \t %i M
        R = Research    \t %i+ M

        B = Rebrand     \t %i M
        S = Price Cut   \t free   # not implemented

        M = Show the market

        [space] = Next Turn

        \t\t\t\t  Q = Quit game instantly


        """ % (engine.PRODUCTION_COST, player.research_cost(), engine.REBRAND_COST) )
        try:
            ch = getch()
        except:
            ch = input ("> ")

        if ch.upper() in ["R", b"R"]:
            research(player)

        elif ch.upper() in ["B", b"B"]:
            rebrand(player, game)

        elif ch.upper() in ["C", b"C"]:
            design(player, game)

        elif ch.upper() in ["S", b"S"]:
            print("not implemented")

        elif ch.upper() in ["M", b"M"]:
            showMarket(player, game)
            try:
                getch()
            except:
                input ()

        elif ch.upper() in [b" ", b'\r', "", " "]:
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
        G = General Compute             %i M  (Not implemented)
        X = Experimental                   M  (Not implemented)

        N = Smaller process node        %i M

        [space] = Exit

        """ % (player.research_cost(), player.research_cost(), player.node_cost() ) )
        # This could work so, that the specific version gives double sciense, but is reset every node.
        # Experimental could be "i feel lucky" boost ranging from 0 to 10 science points randomly
        # Experimental things cost twice the normal research, but may sometimes yeald great leaps in performance

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

        elif ch.upper() in [b" ", b'\r', "",  " "]:
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
    MARKET SITUATION:""")

    if player.products == []:
        print("\n\tIt's a virgin market")

    print('\t Name \t Perf \t Cost \t Price \t Sales \t Size  \t\tNode')
    for p in game.players:
        # print("")
        for c in p.products:
            if c.inproduction == True:
                line = '\t ' + c.name + '\t ' + str(c.perf) + '\t ' + str(round(c.chipCost()))  + '\t ' + str(c.price) + ' c\t ' + str(round(c.sales(game))) + 'k \t ' + str(c.size) + ' mm2 \t' + str(calc.NODE[c.node])
                print(line)
    #try:
    #    getch()
    #except:
    #    input()


def rebrand(player, game):
    """
    You can change the:
     - Name
     - overclock
     - and the price of the chip
    """

    print("""
    ========================================================
    You can change the:
     - Name
     - overclock
     - and the price of your product
     """)

    if player.products == []:
        print("You have no products.\n\nFirst design a product. \nIf you need to make adjustents to it you can make them here.")
        print("========================================================\n")

        try: getch()
        except: input()
    else:
        number = 1
        for c in player.products:
            if c.inproduction == True:
                print('\t Name \t Perf \t Cost \t Price \t Sales \t Size  \t\tNode')
                line = '\t' + str(number) + '\t ' + c.name + '\t ' + str(c.perf) + '\t ' + str(round(c.chipCost()))  + '\t ' + str(c.price) + ' c\t ' + str(round(c.sales(game))) + 'k \t ' + str(c.size) + ' mm2 \t' + str(calc.NODE[c.node])
                print(line)
                number += 1

        i = input("Choose a product to rebrand, Q to quit (1-3):\n> ")
        true_index = -1
        try:
            search_index = int(i-1)
            while search_index > 0:
                for c in player.products:
                    if c.inproduction == True:
                        print('\t Name \t Perf \t Cost \t Price \t Sales \t Size  \t\tNode')
                        line = '\t' + str(number) + '\t ' + c.name + '\t ' + str(c.perf) + '\t ' + str(round(c.chipCost()))  + '\t ' + str(c.price) + ' c\t ' + str(round(c.sales(game))) + 'k \t ' + str(c.size) + ' mm2 \t' + str(calc.NODE[c.node]) 
                        search_index -= 1
                    true_index += 1

            print(line)
            i = true_index
            nuff_money = player.purchase(engine.REBRAND_COST)
            if nuff_money:
                game.remove_from_market(player.products[i])                # Remove the old product from market
                name = input("\nNew chip name: ")
                player.products[i] = set_overdrive(player, player.products[i])
                player.products[i] = set_price(player.products[i])
                game.newProduct(player.products[i])                        # Add the rebranded product back to market
                productReleace(player, player.product[i], game, True)
            else:
                print("Not enough money!")
                try: getch()
                except: input()

        except TypeError:
            print("Cancel")
            pass


def set_overdrive(product):
    "Fine tune the product"

    while True:
        print("OVERDIRVE:")
        print("Basically, level of factory overclock in %%.")
        print("However, not all chips can reach the desired speed within power, thermal and stability constrains.")
        print("default value of Zero is the level that exactly half the chips could do better and half would be lost.")
        print("""
        Examples:
        99%  90%  80%  70%  60%  50%  40%  30%  20%  10%  1%   pass rate
       -23  -13   -9   -6   -3    0    3   -6   -9   13   23   overclock / underclock
        """)
        print("Choose your cut off point:")
        try:
            overdrive = float(input("> "))  #input("Overdrive:\n\t\t\t\t-24 = 99%, \n\t\t\t\t-13 = 90%, \n\t\t\t\t -9 = 80%, \n\t\t\t\t  0 = nominal (50%), \n\t\t\t\t  9 = top 20%, \n\t\t\t\t 13 = top 10%\n\n> ") )
        except ValueError:
            overdrive = 0
        product.overdrive = overdrive
        chipcost = product.chipCost()
        print( "" )
        print( "Manufacturing cost per chip: \t", round( chipcost, 2), "c" )
        print( "Manufacturing yeald:         \t", round( product.yealdPr()*100 ), "%" )
        print( "Total yeald:                 \t", round( product.yealdPr() * product.skewYeald() *100 ), "%" )

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
    return product


def set_price(product):
    chipcost = product.chipCost()
    print("\nChoose chip price:")
    print("Press enter for default (10%%) margin price: (%i c) \nor enter a price." % round(chipcost*1.1) )  # minimum ~26
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
    product.price = price
    return product


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
    #
    player.products[-1] = set_overdrive(player.products[-1])


    # PRICE SELECTION
    #
    player.products[-1] = set_price(player.products[-1])

    # Is the maximum number of chips reached?
    if len(player.products) >= engine.MAX_CHIPS:
        print("""
        Maximum number of chips reached.
        The oldest chip will be removed:
        """)
        print(player.products[0].name, player.products[0].node, player.products[0].size, "mm2", player.products[0].price, "c")
        old_chip = player.products[0]
        game.remove_from_market(old_chip)
        del[player.products[0]]

    # PRODUCTION AND TRANSACTION
    statusBar(player)
    print("""
    It costs %i M to start production.
    Do you whant to procede with producing this chip? (Y/n)
    """ % engine.PRODUCTION_COST)
    try:
        ch = getch()
    except:
        ch = ch = input("")

    if ch.upper() in [b'Y', b' ', b'\r', 'Y', ' ', '']:
        done = player.purchase(engine.PRODUCTION_COST)

        if done == True:

            player.products[-1].inproduction = True
            # market_segment = player.products[-1].market()
            game.newProduct(player.products[-1])                       # Relevant data is updated to game (and market status)   #market_segment, price, player.products[-1].performance())
            # player.income += player.products[-1].get_income(game)				# PROBLEMATIC!!! GET INCOME ASKS FOR GAME PTP THAT IS NONE
            # game.ref_market += player.products[-1].market()
            # game.num_products += 1

            print("Transaction complete\nChip Released\n")
            productReleace(player, player.products[-1], game)			# Announcement and review

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


