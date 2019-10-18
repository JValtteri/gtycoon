#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.08.2019
# UI

import calc
import sys
import engine
import saveload

import time
try:
    from msvcrt import getch
except: pass

SHORT_SLEEP = 0.4
MEDIUM_SLEEP = 1
LONG_SLEEP = 2

def intro():

    time.sleep(SHORT_SLEEP)
    print("""

    You are the CEO of a rising star of semiconductors.

    Steer your company to greatness. Design a product line-up, optimize 
    and tune for profit.

    ...

    """)

def mainmenu():
    license="""
    GTYCOON, copyright (C) 2019 JValtteri
    GTYCOON comes with ABSOLUTELY NO WARRANTY.
    This is free software, you are welcome to 
    redistribute it under certain conditions; 
    for more information, see LICENSE or GPLv2.
    """
    print("\n\n\n\n"+license)

    time.sleep(MEDIUM_SLEEP)
    #try: getch()
    #except: input()

    print("""



     GGG     TTTTT Y   Y  CCC  OOO   OOO  N   N
    G          T    Y Y  C    O   O O   O NN  N
    G GGG ###  T     Y   C    O   O O   O N N N
    G   G      T     Y   C    O   O O   O N  NN
     GGGG      T     Y    CCC  OOO   OOO  N   N



      Q - QUICK GAME (P vs AI)


      N - NEW GAME
      C - CONTINUE


      X - I'M NOT READY FOR THIS


    """)
    while True:
        try: ch = getch()
        except: ch = input()
        if ch.upper() in ["N", b"N"]:
            players = choose_players()
            return engine.GameStatus(players[0], players[1])
        elif ch.upper() in ["Q", b"Q"]:
            return engine.GameStatus(1,1)
        elif ch.upper() in ["X", b"X"]:
            sys.exit("quit")
        if ch.upper() in ["C", b"C"]:
            game = saveload.loadGame()
            if game == None:
                 pass
            #    print("No save found")
            else:
                 return game


def choose_players():
    time.sleep(SHORT_SLEEP)
    human = int( ask("Number of human players: ", 1) )
    time.sleep(SHORT_SLEEP)
    ai = int( ask("Number of AI players: ", 1) )
    time.sleep(SHORT_SLEEP)
    return (human, ai)


def ask(question="", mode=0):
    """
    mode 0 = str
    mode 1 = int (positive)
    """
    while True:
        question = question
        #print("\n")
        answer = input(question)
        #print("\n")
        if answer != '':
            if mode == 1:
                try:
                    if int(answer) >= 0:
                        break
                except ValueError:
                    pass
            else:
                break
    return answer


def productReleace(player, product, game, mode=None):
    "Announcement of a new product and a brief review"

    review_word = "in mid range"
    review = product.name + " is a new, compelling offering from \n" + player.name + " and delivers on their promice to deliver more performance \nin its segment."

    if product.price > 300:
        review_word = "in the hign-end market"

    elif product.price < 100:
        review = "It is an interesting offering in the budjet segment."

    if mode == "REBRAND":
        review_word = "rebrand " + review_word
    elif mode == "PRICEDROP":
        review_word = "pricedrop " + review_word

    # MAXIMUM PERFORMANCE
    perf_max = game.max_perf

    if product.perf == perf_max:
        review = "The new product sets the standard for technology to come."
        if product.ptp >= game.best_ptp:
            review_word = review_word + " to universal acclaim."
    elif product.ptp >= game.best_ptp:
        review = product.name + " is the best thing since sliced bread. It is the best value \nout there."
    elif product.ptp > game.best_ptp * 0.9:
        review = product.name + " offers great value that is hard to beat in the current \nmarket."
    elif product.ptp <= game.best_ptp * 0.6:
        review = product.name + " frankly, is an underwhelming and a thoroughly \nuninteresting product in an already \ncompetitive market."
    elif product.ptp <= game.best_ptp * 0.4:
        review = product.name + " frankly, is an example of the never ending greed of modern \ncompanies ripping off their customers.\nShurely " + player.name + " could do better."


    # PACKAGE THE ANNOUNCEMENT
    print("========================= TECH POINT ==========================\n")
    print(player.name, "released", product.name,  review_word, "\n")
    print(review)
    print("===============================================================")
    time.sleep(MEDIUM_SLEEP)


def statusBar(player):
    print("""

        company:  %s    \t\t   year:     %i
        credits:  %s   \t\t   products: %i
        science:  %i   \t\t\t   income:   %s
        general:  %i    \t\t\t   node:     %s
                        \t\t   defect
                        \t\t   dencity:  %s

    ===============================================================
    """ % (player.name, 
           player.year, 
           calc.scale(player.credits), 
           len(player.products), 
           player.science, 
           calc.scale(player.income), 
           player.generalization, 
           calc.NODE[player.node], 
           str(round(player.refinememt, 3)) 
          ))

def gameScreen(player, game):
    while True:

        statusBar(player)

        print("""
        C = Chip Design \t %s
        R = Research    \t %s+

        B = Rebrand     \t %s
        S = Price Cut   \t free

        M = Show the market

        [space] = Next Turn

        \t\t\t\t  Q = Quit game instantly


        """ % (calc.scale(engine.PRODUCTION_COST), calc.scale(player.research_cost()), calc.scale(engine.REBRAND_COST)) )

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
            priceDrop(player, game)

        elif ch.upper() in ["M", b"M"]:
            showMarket(player, game)
            time.sleep(SHORT_SLEEP)
            #try:
            #    getch()
            #except:
            #    input ()

        elif ch.upper() in [b" ", b'\r', "", " "]:
            if game.num_products < 1:
                print("What sort of a company doesn't have any products!?")
                time.sleep(LONG_SLEEP)

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
        S = Specific Architecture       %s
        G = General Compute             %s\t(Not implemented)
        X = Experimental                    \t(Not implemented)

        N = Smaller process node        %s

        [space] = Exit

        """ % (calc.scale(player.research_cost()), calc.scale(player.research_cost()), calc.scale(player.node_cost()) ) )
        # This could work so, that the specific version gives double sciense, but is reset every node.
        # Experimental could be "i feel lucky" boost ranging from 0 to 10 science points randomly
        # Experimental things cost twice the normal research, but may sometimes yeald great leaps in performance

        try:
            ch = getch()
        except:
            ch = input("> ")


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
            time.sleep(MEDIUM_SLEEP)


        try:
            if researched == True:
                print("Researched!")
            elif researched == False:
                print("Not enough credits")
            elif researched == 404:
                print(
                    "Researchers tried to split an atom, but fission occoured.\n"
                    "Fission produces lots of power but also distroys electronics\n"
                    "so no good.\n"
                    "We'll have to try something else."
                    )
            else:
                print("woops\nScience department made a blunder.\nAlso the game has a bug.\nPlease report this.")

            time.sleep(MEDIUM_SLEEP)
            #try:
            #    getch()
            #except:
            #    input ()
        except:
            pass


def showMarket(player, game):
    "Prints the market situation"
    print("""
    MARKET SITUATION:""")

    if player.products == []:
        print("\n\tIt's a virgin market")

    print('\t Name \t Perf \t Cost \t Price \tSales \t Size  \t\tNode  \tPTP \tRevenue')
    for p in game.players:
        # print("")
        for c in p.products:
            if c.inproduction == True:
                showLine(c, game, None)
                time.sleep(0.2)
    time.sleep(SHORT_SLEEP)


def showLine(product, game, index=None):
    categories = ['\t ',
                  product.name, '\t ',
                  calc.scale( product.perf ), '\t ',
                  str( round( product.chipCost() ) ), '\t ',
                  str( product.price ), ' c\t',
                  calc.scale( product.sales(game) ), '\t ',
                  str( product.size ), ' mm2 \t',
                  str( calc.NODE[product.node] ), '\t',
                  str( round( product.ptp/game.best_ptp, 2 ) ), '\t',
                  calc.scale( product.income ), '\t'
                  #calc.scale( product.market() * 10**7 * product.perf/game.max_perf)
                 ]

    line = ''.join(categories)
    if index != None:
        line = ''.join(('\t ', str(index), line))
    print(line)


def rebrand(player, game):
    """
    You can change the:
     - Name
     - overclock
     - and the price of the chip
    """

    print("""
    ===============================================================
    You can change the:
     - Name
     - overclock
     - and the price of your product
     """)

    if player.products == []:
        print("You have no products.\n\nFirst design a product. \nIf you need to make adjustents to it you can make them here.")
        print("===============================================================\n")

        #try: getch()
        #except: input()
        time.sleep(MEDIUM_SLEEP)


    else:
        number = chooseProduct(player, game, 'rebrand')
        if number is not None:
            i = number
            nuff_money = player.purchase(engine.REBRAND_COST)
            if nuff_money:
                game.remove_from_market(player.products[i])                # Remove the old product from market
                player.products[i].name = input("\nNew chip name: ")
                player.products[i] = set_overdrive(player.products[i])
                player.products[i] = set_price(player.products[i])
                game.newProduct(player.products[i])                        # Add the rebranded product back to market
                productReleace(player, player.products[i], game, "REBRAND")

            else:
                print("Not enough money!")
                time.sleep(MEDIUM_SLEEP)
                #try: getch()
                #except: input()


def priceDrop(player, game):
    i = chooseProduct(player, game, 'pricedrop')
    if i is not None:
        game.remove_from_market(player.products[i])                # Remove the old product from market
        player.products[i] = set_price(player.products[i])
        game.newProduct(player.products[i])                        # Add the rebranded product back to market
        productReleace(player, player.products[i], game, "PRICEDROP")
    else:
        pass


def chooseProduct(player, game, text):
    number = 1
    print('\t No. \t Name \t Perf \t Cost \t Price \tSales \t Size  \t\tNode  \tPTP \tRevenue')

    for c in player.products:
        if c.inproduction == True:
            showLine(c, game, number)
            number += 1

    i = ask("Choose a product to %s, Q to quit :\n> " % text , 1)
    cancel = False
    try:
        number = int(i)-1

    except ValueError:
        print("Cancel")
        cancel = True
    except IndexError:
        print("You don't have a product with that index.\nCancelling:")
        time.sleep(MEDIUM_SLEEP)
        cancel = True

    if cancel is not True:
        product = player.products[number]
        print('\t Name \t Perf \t Cost \t Price \tSales \t Size  \t\tNode  \tPTP \tRevenue')

        showLine(product, game, None)

        return number
    else:
        return None


def set_overdrive(product):
    "Fine tune the product"

    while True:
        print("OVERDIRVE:")
        print("Basically, level of factory overclock in (%).")
        print("However, not all chips can reach the desired speed within power, thermal and stability constrains.")
        print("default value of Zero is the level that exactly half the chips could do better and half would be lost.")
        print("""
        Examples:
        99%  90%  80%  70%  60%  50%  40%  30%  20%  10%  1%   pass rate
       -23  -13   -9   -6   -3    0    3    6    9   13   23   underclock / overclock
        """)
        print("Choose your cut off point:")
        try:
            overdrive = float(input("> "))  #input("Overdrive:\n\t\t\t\t-24 = 99%, \n\t\t\t\t-13 = 90%, \n\t\t\t\t -9 = 80%, \n\t\t\t\t  0 = nominal (50%), \n\t\t\t\t  9 = top 20%, \n\t\t\t\t 13 = top 10%\n\n> ") )
        except ValueError:
            print(
            "\tYou didn't specify a value.\n"
            "\tUsing a conservative default: -13.\n"
            "\tThat way 90% of the chip will meet spec.\n"
            )
            time.sleep(MEDIUM_SLEEP)

            overdrive = -13
        product.overdrive = overdrive
        chipcost = product.chipCost()
        print( "" )
        print( "Manufacturing cost per chip: \t", round( chipcost, 2), "c" )
        print( "Manufacturing yeald:         \t", round( product.yealdPr()*100 ), "%" )
        print( "Total yeald:                 \t", round( product.yealdPr() * product.skewYeald() *100 ), "%" )

        print("\nProceed?")
        try:
            ch = getch()
        except:
            ch = input("(Y/n) ")

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
    print("Press enter for default (10%%) margin over manufacturing price: (%i c) \nor enter a sale price." % round(chipcost*1.1) )  # minimum ~26
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
         #try:
         #    getch()
         #except:
         #    input()'
         time.sleep(MEDIUM_SLEEP)
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
    print("\n\n\n")

    # Asks if there is a new chip designed, that is not in production
    try:
        no_saved = player.products[-1].inproduction
    except:
        # If there are no chips at all, there are no saved chips either
        no_saved = True

    # START FRESH
    # THE BASICS
    if no_saved:
        name = ask("Chip name: ", 0)
        time.sleep(SHORT_SLEEP)
        size = int( ask("Chip size [mm2]: ", 1) )
        time.sleep(SHORT_SLEEP)
        price = 1
        overdrive = 0

        new_product = engine.Product(name, size, overdrive, price, player.node, player.science, player.refinememt)

        # The chip is added to products (saved), it will be refrenced to as
        # player.products[-1] ig. Players newest product.
        player.products.append(new_product)

    # RECALL AN UNFINISHED CHIP
    #
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


    # ENFORCE MAXIMUM NUMBER OF CHIPS
    #
    if len(player.products) > engine.MAX_CHIPS:
        print("""
        Maximum number of chips reached.
        Pick on chip to be removed:
        """)
        time.sleep(MEDIUM_SLEEP)

        number = chooseProduct(player, game, 'replace')
        if number == None:                                          # If none selected, the oldest (0) will be removed
            number = 0
        old_chip = player.products[number]
        game.remove_from_market(old_chip)
        del[player.products[number]]


    # PRODUCTION AND TRANSACTION
    #
    statusBar(player)
    print("""
    It costs %s to start production.
    Do you whant to procede with producing this chip? 
    (Y/n)""" % calc.scale(engine.PRODUCTION_COST))
    try:
        ch = getch()
    except:
        ch = input("")

    if ch.upper() in [b'Y', b' ', b'\r', 'Y', ' ', '']:
        done = player.purchase(engine.PRODUCTION_COST)

        if done == True:
            player.products[-1].inproduction = True
            game.newProduct(player.products[-1])                       # Relevant data is updated to game (and market status)   #market_segment, price, player.products[-1].performance())
            print("Transaction complete\nChip Released\n")
            productReleace(player, player.products[-1], game)          # Announcement and review
            showMarket(player, game)
        else:
            print("Not enough credits!")
        #try: getch()
        #except: input()
        time.sleep(MEDIUM_SLEEP)

    elif ch.upper() in ['N', b'N']:
        print("""
        Do you whant to save the chip for later?
        (Y/n)""")
        try:
            getch()
        except:
            ch = input("")
        if ch.upper() in ['N', b'N']:
            del player.products[-1]
            print("Deleted")
        else:
            pass
