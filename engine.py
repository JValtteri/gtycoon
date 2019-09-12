#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.08.2019
# engine

import calc
import UI
#from msvcrt import bgetch
from math import log, e, sqrt
#from gtycoon import game

# ddencity=[0.4, 0.3, 0.2, 0.1, 0.05]
REFINEMENT = 0.4            # Normal defect dencity (1/cm2) of a new node
RESEARCH_BASE_COST = 10     # Cost to research the first level
NODE_BASE_COST = 100        # Cost to research the first node
PRICE = 0.207972270         # Silicone price per mm2
AVGCONSUMER = 200.0         # Money an average consumer has to spend
TOTAL_MARKET = 10000        # Size of the annual market in thousands
REFINE = 1.3                # Refinement step per year
MAX_CHIPS = 4               # Maximum allowed chips per player
PRODUCTION_COST = 1 # Cost to start manufacturing a new chip

class GameStatus():
    """
    Keeps track of the game state.

    Inputs:
    number of human players
    number of ai players
    """

    def __init__(self, human_players, aiPlayers):
        self.ref_market = 0              # Initial "refrence market yeald"
        self.sum_price = 0               # Sum price of all active products
        self.sum_perf = 0
        self.num_products = 0            # Number of active products
        self.players = []
        self.avg_ptp = 0                 # Average price to performance

        for id in range(human_players):
            self.players.append(Player(id))
            number = id

        for i in range(aiPlayers):
            id = number + i
            self.players.append(Player(id, name="ASIx", ai=True))

    def newProduct(self, product):
        market = product.market()
        price = product.price
        perf = product.perf

        self.num_products += 1
        self.ref_market += market
        self.sum_price += price
        self.sum_perf += perf

        self.update_ptp()

    def remove_from_market(self, product):
        market = product.market()
        price = product.price
        perf = product.perf

        self.num_products -= 1
        self.ref_market -= market
        self.sum_price -= price
        self.sum_perf -= perf

        self.update_ptp()

    def update_ptp(self):
        try:
            ptp = self.sum_price/self.sum_perf
            self.avg_ptp = ptp
        except ZeroDivisionError:
            self.avg_ptp = 0

    # def price_cut(self, old_market, new_market, old_price, new_price):
    #     pass


class Player():

    def __init__(self, id = 0, name = "Mixel Co.", ai = False):

        self.name = name
        self.id = id
        self.credits = 3     # thousand credits
        self.science = 1        #science level
        self.generalization = 1 # resistance to technology changes
        self.node = 0
        self.year = 1978
        self.products = []              # List of all products
        self.refinememt = REFINEMENT    # Defect dencity of current node
        self.income = 0
        self.ai = ai

    def research_cost(self):
        "returns the cost of new research"

        cost = RESEARCH_BASE_COST * 1.1 ** (self.science + self.generalization - 1)

        return cost

    def research(self, branch=0):
        "Buy a research point to a selected branch"
        nuff_money = Player.purchase(self, Player.research_cost(self))
        if nuff_money:
            if branch == 0:
                self.science += 1
                return True
            elif branch == 1:
                self.generalization += 1
                return True
            #elif branch == 2:
            #    self.node += 1
            #    return True
        else:
            return False

    def node_cost(self):
        "returns the cost of new research"

        cost = NODE_BASE_COST * 1.1 ** (self.node)

        return cost

    def research_node(self):
        "Buy a research point to a selected branch"
        nuff_money = Player.purchase(self, Player.node_cost(self))
        if nuff_money:
            self.node += 1
            # When moving to a new node, the node refinement is reset
            self.refinememt = REFINEMENT
            return True
        else:
            return False

    def purchase(self, cost):
        """
        Checks if transaction can be completed
        deducts payment and returns: 
          True for succesfull transaction and
          False for no sale.
        """
        if cost <= self.credits:
            self.credits = self.credits - cost
            return True
        else:
            return False


class Product():

    def __init__(self, name, size, overdrive, price, node, science, refinememt=0.4):
        self.name = name                        # Name of the product
        self.size = size                        # Chip size in mm2
        self.node = node                        # Manufacturing node (eg. 28 nm)
        self.science = science                  # science level
        self.overdrive = overdrive              # how agressively the chips are binned
        self.refinememt = refinememt            # defect dencity in x/cm2
        self.yeald = self.yealdPr()             # production yeald of the physical chips
        self.mcost = self.chipCost()            #
        self.cost = self.chipCost()             # cost to manufacture
        self.price = price                      # sale price
        # self.income = 0                         # income is created automatically every turn
        self.inproduction = False               # is the chip in the market
        self.perf = self.performance()          # performance metric
        self.price_delta = 0                    # Delta from the
        self.ptp = 0

        self.update_ptp()                       # Price to performance


        # self.update_price_delta()    # Difference in price to performance to the market average
                                       # is created automatically every turn

    def market(self):
        "Counts the total size of a market segment"
        market = calc.normal(self.price / AVGCONSUMER)
        #market = totalMarket * ( normal(max) - normal(min) )
        return market

    def sales(self, game):
        "Counts number of units sold per year"
        self.update_price_delta(game)
        theoretical_sales = self.market() / game.ref_market * TOTAL_MARKET
        if game.avg_ptp == 0:
            print("AVG PTP defined!")  # DEBUG
            return 0
        else:
            # DEBUG
            # print("ptp self", self.ptp, "avg", game.avg_ptp)
            # print("raw sales", theoretical_sales)
            # print("ptp modifier", game.avg_ptp/self.ptp)  # calc.normal(game.avg_ptp/self.ptp * 100) * 2 )
            sales = theoretical_sales * ( calc.normal(game.avg_ptp/self.ptp) * 2 ) # * ( 1 + self.price_delta ) #  modifiers (price to performance)
        return sales

    def get_income(self, game):
        "Counts the total winnings from the products sold"
        income = (self.sales(game) * (self.price - self.cost)) / 1000
        return income

    def update_income(self, game):
        "updates the income"
        self.income = self.get_income(game)

    def performance(self):
        "Calculate the normaliced performance index of a chip (skew)"
        performance = ( 1.1**self.science * self.size * (1 + self.overdrive/100.0) ) * 2 ** self.node
        return round(performance)

    def howhot(self):
        "gives a number reprecenting how much power the chip consumes"
        return self.size * self.overdrive ** 2

    def skewYeald(self):
        "calculate the procent of chips fit for a skew"
        return 1-calc.normal(self.overdrive, 1)

    def yealdPr(self):
        "Calculate the *process* yeald in procent"

        # VERY IMNPORTANT!
        #
        # Defect dencity is often given in  sq cm
        # while chip size is given in       sq mm
        # the difference is (100x)!!
        #
        # The formula works only if both inputs are in same units!!!

        # THE CONVERSION IS DONE HERE!
        rdencity = self.refinememt/100

        #poisson = e ** -(self.size * ddencity[self.refinememt])
        murphy = ( ( 1.0 - e ** -(self.size * rdencity) ) / (self.size * rdencity) ) ** 2.0

        return murphy

    def update_yeald(self):
        self.yeald = self.yealdPr()
        #print("YealdPr" , self.yealdPr())

    def chipCost(self):
        "Calculate the actual manufacturing cost per chip"
        chip_yeald = self.yeald
        skew_yeald = self.skewYeald()

        # print("chip", chip_yeald)
        # print("skew", skew_yeald)

        price = self.size * PRICE * 1/chip_yeald * 1/skew_yeald
        return price

    def update_cost(self):
        "Updates the manufacturing cost per chip"
        self.cost = self.chipCost()

    def update_price_delta(self, game):
        "Calculattes the price delta from market average"
        delta = self.price - ( game.sum_price / game.num_products )
        return delta

    def update_refinement(self):
        self.refinememt = self.refinememt / REFINE

    def update_ptp(self):
        ptp = self.price / self.perf
        self.ptp = ptp


if __name__ == "__main__":

    game = GameStatus(1,0)
    player = game.players[0]
    products = player.products
    new_product = Product("chip A", 100, 0, 100, 1, 1)
    products.append(new_product)
    game.newProduct(products[-1])
    new_product = Product("chip B", 100, 0, 100, 2, 1)
    products.append(new_product)
    game.newProduct(products[-1])


    # UPDATE EVERYTHING

    game.update_ptp()

    #for p in products:
    #    p.update_market()

    # SHOW RESULTS

    print(products[0].name, products[0].price, products[0].perf, int(products[0].sales(game)) )
    print(products[1].name, products[1].price, products[1].perf, int(products[1].sales(game)) )

    #newProduct = Product("name", 50, 0, 200, 0, 0)
    #products = []
    #products.append(newProduct)
    # ref_market += products[-1].market()
    # num_products += 1


    # print(ref_market)
    # print(num_products)

    # print(products[-1].market())
    # print(products[-1].sales())
