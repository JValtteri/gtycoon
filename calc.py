#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 16.08.2019
# GPU-tycoon Calculator

'''
All game calculations
'''

NORMAL = [.5000, .5398, .5793, .6179, .6554, .6915, .7257, .7580, .7881, .8159, .8413, .8643, .8849, .9032, .9192, .9332, .9452, .9554, .9641, .9713, .9772, .9821, .9861, .9893, .9918, .9938, .9953, .9965, .9974, .9981, .9987, .9990, .9993, .9995, .9997]

# variable [node] is an index of list NODE
NODE = ["3 µm", "2 µm", "1.5 µm", "1 µm", "700 nm", "500 nm", "350 nm", "250 nm", "180 nm", "130 nm", "90 nm", "65 nm", "45 nm", "32 nm", "22 nm", "15 nm", "10 nm", "7 nm", "5 nm", "3.5 nm", "2.5 nm", "1.8 nm", "1.3 nm", "0.9 nm"]

# WAFER_PRICE=12000

from math import log, e, sqrt
import math

def normal(procent, mode=0):
    """
    Returns the normal prosentage below [procent]
    Default (mode 0) is logarithmic
    (mode 1) is natural 
    """

    # Calculates, how meny steps of 10% are in [procent]
    # More procisely, what is the 1.1 base logarithm of [procent]
    # This defines the steps on the [NORMAL] scale and the received lookup value.

    if procent == 0:
        # delta = 0
        precentile = NORMAL[0]
    elif procent < 0:
        if mode == 0:
            delta = round( log(-procent, 1.1) )
        else:
            delta = round(-procent)
        if delta > 34:
            return 0.0
        elif delta < -34:
            return 1.0
        elif delta < 0:
            print("woops")
        else:
            precentile = 1.0 - NORMAL[delta]
    else:
        if mode == 0:
            delta = round( log(procent, 1.1) )
        else:
            delta = round(procent)
        if delta < -34:
            return 0.0
        elif delta > 34:
            return 1.0
        elif delta < 0:
            precentile = 1.0 - NORMAL[-delta]
        else:
            precentile = NORMAL[delta]
    return precentile


if __name__ == "__main__":
    #a = input("give procent > ")
    #print(normal(float(a)))

    # a = float(input("size mm^2: "))
    # b = float(input("dencity  : "))
    # c = float(input("overdrive: "))

    #print(chipCost(a, c, b))

    procent = float( input("procent > ") )
    print(normal(procent, 1))

    # 1-calc.normal(self.overdrive, 1)

